# Cifrado con AES-256 en modo CTR y uso de PBKDF2


## Ejecución
```
$ python3 encrypt.py
```

## Instalación de paquetes
```
# apt install mariadb-server python3-pycryptodome python3-mysqldb python3-securestring
```

## Generar esquema de la base de datos
```
# mysql < hospital_scheme.sql
```

## Versiones
- Debian GNU/Linux 12
- Mariadb 10.11.6 
- Python 3.11.2
- PyCryptodome 3.11.0
- MySQLdb 1.4.6
- SecureString 0.2

## Referencias
- https://cryptobook.nakov.com/
- https://pycryptodome.readthedocs.io/
- https://mysqlclient.readthedocs.io/
- https://www.sjoerdlangkemper.nl/2016/05/22/should-passwords-be-cleared-from-memory/
- https://www.sjoerdlangkemper.nl/2016/06/09/clearing-memory-in-python/
