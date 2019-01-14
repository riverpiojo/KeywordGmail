# Importing required libraries
from datetime import datetime
import datetime
import csv
import sys
import re
import time
import base64
def libreriasnecesarias():
    print "CRITICAL FALTAN ALGUN PAQUETE PYTHON NECESARIO PARA EJECUTAR EL SCRIPT"
    print "SE NECESITA TENER INSTALADO PIP"
    print "INSTALAR PIP DEBIAN O DERIBADOS"
    print "     sudo apt install python-pip"
    print "INSTALL PIP CENTOS O DERIBADOS"
    print "     sudo yum install epel-release"
    print "     sudo yum install python-pip"
    print "PARA INSTALAR LOS PAQUETES EJECUTAR"
    print "     sudo pip install --upgrade google-api-python-client oauth2client httplib2 bs4 bdateutil mysql-connector"

try:
    from oauth2client import file, client, tools
    from apiclient import discovery
    from apiclient import errors
    from httplib2 import Http
    from bs4 import BeautifulSoup
    import dateutil.parser as parser
    import mysql.connector
    import ConfigParser
except Exception, e:
    print e
    libreriasnecesarias()
    sys.exit(1)

def variables():
    config = ConfigParser.ConfigParser()
    config.read("config.ini")
    for i in "mysql_user mysql_db mysql_pass mysql_host mysql_port mysql_table mysql_table_id mysql_table_from mysql_table_asunto mysql_table_date".split():
        globals()['%s' % i] = config.get('mysql', i)
    for i in "credenciales user_id label_id_one label_id_two storage_json".split():
        globals()['%s' % i] = config.get('gmail', i)
        
def conectar_gmail():
    #Autenticacion https://developers.google.com/gmail/api/quickstart/python 
    # Creating a storage.JSON file with authentication details
    SCOPES = 'https://www.googleapis.com/auth/gmail.modify' # we are using modify and not readonly, as we will be marking the messages Read
    store = file.Storage(storage_json) 
    creds = store.get()
    #si no existe el storage va a crear uno
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(credenciales, SCOPES)
        creds = tools.run_flow(flow, store)
    GMAIL = discovery.build('gmail', 'v1', http=creds.authorize(Http()))
    return GMAIL

def marcar_email_leido(GMAIL,m_id):
    try:
        GMAIL.users().messages().modify(userId='me', id=m_id,body={ 'removeLabelIds': ['UNREAD']}).execute()
    except Exception, e:
        print e
        print "CRITICAL NO PUDE MARCAR COMO LEIDO EL EMAIL"

def connect_databse_mysql():
    try:
        mymysql = mysql.connector.connect(host=mysql_host,user=mysql_user,passwd=mysql_pass,port=mysql_port)
    except Exception, e:
        print e
        print "CRITICAL NO PUDE CONECTAR A LA BASE DE DATOS REVISAR QUE LA BASE ESTE ARRIBA O QUE EL HOST USER Y PASS SEAN CORRECTOS"
        sys.exit(1)
    mycursor = mymysql.cursor()
    mycursor.execute("SHOW DATABASES")
    flag = 0
    for i in mycursor:
        if mysql_db in i:
            flag = 1 
    if flag == 1:
        try:
            mymysql.close()
            mymysql = mysql.connector.connect(host=mysql_host,user=mysql_user,passwd=mysql_pass,port=mysql_port,database=mysql_db)
        except Exception, e:
            print e
            print "CRITICAL NO ME PUDE CONECTAR A LA BASE DE DATOS REVISAR SI EL USUARIO TIENE PERMISOS"
    else:
        try:
            print "CREANDO DATABASE"
            mycursor.execute("CREATE DATABASE " + mysql_db)
            mymysql.close()
            mymysql = mysql.connector.connect(host=mysql_host,user=mysql_user,passwd=mysql_pass,port=mysql_port,database=mysql_db)
        except Exception, e:
            print e
            print "CRITICAL NO PUDE CREAR LA BASE DE DATOS REVISAR SI EL USUARIO TIENE PERMISOS"
    mycursor = mymysql.cursor()
    mycursor.execute("SHOW TABLES")
    flag = 0
    for i in mycursor:
        if mysql_table in i:
            flag = 1
    if flag == 0:
        print "CREANDO TABLE"
        mycursor.execute("create table " + mysql_table + " ( " + mysql_table_id + " INT NOT NULL AUTO_INCREMENT, " + mysql_table_asunto + " TEXT NOT NULL, " + mysql_table_from + " TEXT NOT NULL, " + mysql_table_date + " DATE, PRIMARY KEY ( " + mysql_table_id + " ));")
    mymysql.close()
    mymysql = mysql.connector.connect(host=mysql_host,user=mysql_user,passwd=mysql_pass,port=mysql_port,database=mysql_db)	
    return mymysql


def guardar_mysql(devops_email_asunto, devops_email_from, devops_email_date):
    mymysql = connect_databse_mysql()
    try:
        mycursor = mymysql.cursor()
        sql = "INSERT INTO " + mysql_table  + "(" + mysql_table_asunto + "," + mysql_table_from + "," + mysql_table_date +") VALUES (%s, %s, %s)"
        val = (devops_email_asunto, devops_email_from, devops_email_date)
        mycursor.execute(sql, val)
        mymysql.commit()
    except Exception, e:
        print e
        print "CRITICAL NO PUDE INSERTAR EN LA BASE DE DATOS"
        sys.exit(1)

def main():
    variables()
    GMAIL = conectar_gmail()
    unread_msgs = GMAIL.users().messages().list(userId='me',labelIds=[label_id_one, label_id_two]).execute()
    try:
        # We get a dictonary. Now reading values for the key 'messages'
        mssg_list = unread_msgs['messages']
    except Exception, e:
        print e
        print "Bandeja vacia"
        sys.exit(0)
    for mssg in mssg_list:
    	m_id = mssg['id'] # get id of individual message
	message = GMAIL.users().messages().get(userId='me', id=m_id).execute() # fetch the message using API
        body = message['snippet']
	payld = message['payload'] # get payload of the message 
	headr = payld['headers'] # get header of the payload
	for head in headr: # getting the Subject
    	    if head['name'] == 'Subject':
	        msg_subject = head['value']
            elif head['name'] == 'Date':
                msg_date = head['value']
                date_parse = (parser.parse(msg_date))
                m_date = (date_parse.date())
                fecha = str(m_date)
            elif head['name'] == 'From':
                 msg_from = head['value']
            else:
		pass
        if ( "devops" in msg_subject.lower() ) or ( "devops" in body.lower() ) :
            print ("devops en asunto o body", "asunto: ", msg_subject, " fecha: ", fecha,  " from: ", msg_from, " body: " + body)
            guardar_mysql(msg_subject, msg_from, fecha)
            marcar_email_leido(GMAIL,m_id)
if __name__ == '__main__':
        main()
