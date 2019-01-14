# CHALLENGE KEYWORD GMAIL

## OBJETIVO

Armar un programa en Python, Go, Groovy o Java que pueda acceder, de manera automática, a una cuenta
de Gmail, leer los correos e identificar aquellos que tengan la palabra "DevOps" en el Body.
De estos correos identificados, se deberá guardar en una base de datos MySQL los siguientes campos:
● fecha de recepción del correo
● to (remitente que ha enviado el correo)
● subject
Tené en cuenta que solo deberá guardar aquellos correos que ya no haya guardado en alguna corrida
anterior.

### ENTREGABLES

-Código fuente (en zip o url al repositorio)

https://github.com/riverpiojo/KeywordGmail

-Instrucciones para la ejecución de la aplicación (incluida cualquier aplicación o librería a instalar
para el correcto funcionamiento del programa)

Debian 9, mariadb server, cliente pip ($ sudo apt install python-pip), dependencias ($ sudo pip install --upgrade google-api-python-client oauth2client httplib2 bs4 bdateutil mysql-connector ldap).

-Ejecución

$ sudo apt install python-pip ; sudo pip install --upgrade google-api-python-client oauth2client httplib2 bs4 bdateutil mysql-connector
$ python challenge_keyword.py

-Usuario y contraseña de la cuenta de gmail (deberá crear una cuenta específica para este challenge)
para validación de la aplicación.

user: merlib2019@gmail.com
pass: Mercado2019

-Descripción de la aplicación realizada, problemas y soluciones con los que se encontró al realizar la
misma.

Script desarrollado en python con 2 dependecias .json y un config.ini con ciertas variables definidas a utilizar por el script.

---