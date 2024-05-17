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
def cifrar_datos(diagnosis, treatment, key):
    # Generar nuevos nonces para cada cifrado
    diagnosis_nonce = get_random_bytes(8)
    treatment_nonce = get_random_bytes(8)

    # Crear objetos AES para cada cifrado
    diag_aes = AES.new(key, AES.MODE_GCM, nonce=diagnosis_nonce)
    treat_aes = AES.new(key, AES.MODE_GCM, nonce=treatment_nonce)

    # Cifrar los campos sensibles
    diagnosis_ciphertext = diag_aes.encrypt(diagnosis.encode('utf-8'))
    treatment_ciphertext = treat_aes.encrypt(treatment.encode('utf-8'))

    # Codificar en base64
    diagnosis_ciphertext = b64encode(diagnosis_ciphertext).decode('utf-8')
    treatment_ciphertext = b64encode(treatment_ciphertext).decode('utf-8')
    diagnosis_nonce = b64encode(diagnosis_nonce).decode('utf-8')
    treatment_nonce = b64encode(treatment_nonce).decode('utf-8')
    
    return diagnosis_ciphertext, treatment_ciphertext, diagnosis_nonce, treatment_nonce


# Conexión a la base de datos y almacenamiento
try:
    mydb = MySQLdb.connect(user=config.user, password=config.password, database=config.dbname)
    cursor = mydb.cursor()
    
    insert_query = """INSERT INTO expediente (nombre, diagnostico, tratamiento, passwordSalt, diag_nonce, treat_nonce) 
                      VALUES (%s,%s,%s,%s,%s,%s)"""
    
    # Insertar el registro de prueba
    diagnosis_ciphertext, treatment_ciphertext, diagnosis_nonce, treatment_nonce = cifrar_datos('Heridas por ataque de T-800', 'Paracetamol cada 8 hrs', key)
    record_to_insert = ('John Connor', diagnosis_ciphertext, treatment_ciphertext, b64encode(passwordSalt).decode('utf-8'), diagnosis_nonce, treatment_nonce)
    cursor.execute(insert_query, record_to_insert)
    mydb.commit()

    # Recuperar los registros del txt y cifrarlos
    pacientes = lt.recuperar_pacientes()
    for paciente in pacientes:
        name = paciente['name']
        diagnosis = paciente['diagnosis']
        treatment = paciente['treatment']
        
        diagnosis_ciphertext, treatment_ciphertext, diagnosis_nonce, treatment_nonce = cifrar_datos(diagnosis, treatment, key)
        
        record_to_insert = (name, diagnosis_ciphertext, treatment_ciphertext, b64encode(passwordSalt).decode('utf-8'), diagnosis_nonce, treatment_nonce)
        cursor.execute(insert_query, record_to_insert)
        mydb.commit()
    
    print("Inserción exitosa.")
    
except Exception as err:
    print(f"Ocurrió un error")
    sys.exit()

finally:
    if mydb:
        cursor.close()
        mydb.close()
        print("Conexion finalizada")






# Sobrescribir el contenido de las variables para evitar que se
# puedan obtener los datos a través de un volcado de memoria RAM
clearmem(key)
clearmem(password)
clearmem(diagnosis)
clearmem(treatment)


