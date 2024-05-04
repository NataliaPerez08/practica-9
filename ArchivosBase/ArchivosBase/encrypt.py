#!/usr/bin/env python3

# Paulo Contreras Flores [paulo.contreras.flores@gmail.com]
# Tonatihu Sánchez (uso de MySQLdb, PyCryptodome y otros ajustes)

from getpass import getpass
from base64 import b64encode
from SecureString import clearmem
from Cryptodome.Protocol.KDF import PBKDF2
from Cryptodome.Hash import SHA512
from Cryptodome.Random import get_random_bytes
from Cryptodome.Cipher import AES
import MySQLdb, config, sys

# Se obtiene la contraseña para cifrar los datos
password = getpass()

# La idea es que estos datos vengan de otro lado como parte
# de una app más completa.
name = 'John Connor'
diagnosis = bytes('Heridas por ataque de T-800', 'utf-8')
treatment = bytes('Paracetamol cada 8 hrs', 'utf-8')

# El algoritmo de derivación de llaves PBKDF2 necesita una salt,
# por lo que generamos una secuencia pseudoaleatoria de 16 bytes. 
passwordSalt = get_random_bytes(16)

# En esta práctica emplearemos AES-256, por lo que necesitamos
# que el algoritmo de derivación de llaves PBKDF2 nos proporcione
# una llave 256 bits (32 bytes).
key = PBKDF2(password, passwordSalt, 32, count=1000000, hmac_hash_module=SHA512)

# Para el modo de operación CTR, se forma lo que se conoce como "Counter block"
# de longitud 128 bits, y se compone de un "nonce" (number-used-once; valor aleatorio
# de 64 bits) y un contador (que de manera predeterminada comienza en cero)
diagnosis_nonce = get_random_bytes(8)
treatment_nonce = get_random_bytes(8)
diag_aes = AES.new(key, AES.MODE_CTR, nonce=diagnosis_nonce)
treat_aes = AES.new(key, AES.MODE_CTR, nonce=treatment_nonce)

# Cifrado de los campos considerados sensibles
diagnosis_ciphertext = diag_aes.encrypt(diagnosis)
treatment_ciphertext = treat_aes.encrypt(treatment)

# Se codifica en base 64 tanto la passwordSalt como el 
# criptograma para guardarlos en la base de datos
passwordSalt = b64encode(passwordSalt)
diagnosis_ciphertext = b64encode(diagnosis_ciphertext)
treatment_ciphertext = b64encode(treatment_ciphertext)
diagnosis_nonce = b64encode(diagnosis_nonce)
treatment_nonce = b64encode(treatment_nonce)

print('Diagnosis:', diagnosis)
print('Medical treatment:', treatment)
print('PasswordSalt:', passwordSalt)
print('AES encryption key:', key.hex())
print(f"Nonces:- diagnosis:{diagnosis_nonce}; treatment:{treatment_nonce}")
print('Diagnosis encrypted:', diagnosis_ciphertext)
print('Treatment encrypted:', treatment_ciphertext)

mydb = None
# Guardar los datos en una base de datos relacional
try:
    # Leemos las credenciales para la conexión del archivo config.py
    # El cifrado de la conexión se realizará en otra práctica
    mydb = MySQLdb.connect(user=config.user, password=config.password, database=config.dbname)
    cursor = mydb.cursor()
    insert_query = """ INSERT INTO expediente (nombre, diagnostico, tratamiento, passwordSalt, diag_nonce, treat_nonce) 
						VALUES (%s,%s,%s,%s,%s,%s)"""
    record_to_insert = (name, diagnosis_ciphertext, treatment_ciphertext, passwordSalt, diagnosis_nonce, treatment_nonce)
    cursor.execute(insert_query, record_to_insert)

    mydb.commit()
    print("Record inserted successfully with id ", cursor.lastrowid)

except Exception as err:
  print(f"\nSomething went wrong: {err}")
  sys.exit()

finally:
    if mydb:
        cursor.close()
        mydb.close()
        print("DBMS connection is closed")


# Sobrescribir el contenido de las variables para evitar que se
# puedan obtener los datos a través de un volcado de memoria RAM
clearmem(key)
clearmem(password)
clearmem(diagnosis)
clearmem(treatment)

print("\nVariables después de sobreescribir su contenido:")
print(f"AES encryption key: '{key.hex()}'")
print(f"Password: '{password}'")
print(f"Diagnosis:'{diagnosis}'")
print(f"Treatment: '{treatment}'")
