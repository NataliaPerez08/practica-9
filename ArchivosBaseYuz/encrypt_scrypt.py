#!/usr/bin/env python3

# Paulo Contreras Flores [paulo.contreras.flores@gmail.com]
# Tonatihu Sánchez (uso de MySQLdb, PyCryptodome y otros ajustes)
# Equipo los gatitos cuanticos, cifrado AES en modo GCM y algorimo
# de derivación de llaves scrypt

from getpass import getpass
from base64 import b64encode
from hashlib import scrypt
from SecureString import clearmem
from Cryptodome.Random import get_random_bytes
from Cryptodome.Cipher import AES
import MySQLdb, config, sys

import lector_txt as lt
import cifrador as cif

# Se obtiene la contraseña para cifrar los datos
password = getpass()

# El algoritmo de derivación de llaves scrypt necesita una salt,
# por lo que generamos una secuencia pseudoaleatoria de 16 bytes.
passwordSalt = get_random_bytes(16)

password = bytes(password, 'utf-8')
# En esta práctica emplearemos AES-256, por lo que necesitamos
# que el algoritmo de derivación de llaves scrypt nos proporcione
# una llave 256 bits (32 bytes).
key = scrypt(password, salt=passwordSalt, n=2048, r=8, p=1, maxmem=0, dklen=32)

# Modo de operación GCM
diagnosis_nonce = get_random_bytes(8)
treatment_nonce = get_random_bytes(8)
diag_aes = AES.new(key, AES.MODE_GCM, nonce=diagnosis_nonce)
treat_aes = AES.new(key, AES.MODE_GCM, nonce=treatment_nonce)

passwordSalt = b64encode(passwordSalt)
diagnosis_nonce = b64encode(diagnosis_nonce)
treatment_nonce = b64encode(treatment_nonce)

mydb = None
# Guardar los datos en una base de datos relacional
try:
    # Leemos las credenciales para la conexión del archivo config.py
    # El cifrado de la conexión se realizará en otra práctica
    mydb = MySQLdb.connect(user=config.user, password=config.password, database=config.dbname)
    cursor = mydb.cursor()
    
    insert_query = """ INSERT INTO expediente (nombre, diagnostico, tratamiento, passwordSalt, diag_nonce, treat_nonce) 
						VALUES (%s,%s,%s,%s,%s,%s)"""
    
    # Recuperar los registros del txt
    pacientes = lt.recuperar_pacientes()
    for paciente in pacientes:
        name = paciente['name']
        diagnosis = paciente['diagnosis']
        treatment = paciente['treatment']
        
        # Proceder a cifrar los datos
        diagnosis_ciphertext, treatment_ciphertext = cif.cifrar(diagnosis, treatment, diag_aes, treat_aes)
        
        record_to_insert = (name, diagnosis_ciphertext, treatment_ciphertext, passwordSalt, diagnosis_nonce, treatment_nonce)
        print(f"Inserting record: {record_to_insert}")
        
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
