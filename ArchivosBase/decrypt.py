# Modulo que se encarga de descifrar los datos de los pacientes

from base64 import b64decode
from Cryptodome.Cipher import AES
from Cryptodome.Protocol.KDF import PBKDF2
import MySQLdb, config, sys
  

def descifrar(diagnosis_ciphertext, treatment_ciphertext, diag_aes, treat_aes):
    # Decodificar el cifrado
    diagnosis_ciphertext = b64decode(diagnosis_ciphertext)
    treatment_ciphertext = b64decode(treatment_ciphertext)
    
    # Descifrar los campos considerados sensibles
    diagnosis = diag_aes.decrypt(diagnosis_ciphertext)
    treatment = treat_aes.decrypt(treatment_ciphertext)
    
    # Decodificar los bytes a string
    diagnosis = diagnosis.decode('utf-8')
    treatment = treatment.decode('utf-8')

    return diagnosis, treatment


def consultar_pacientes(password):
    
    mydb = MySQLdb.connect(user=config.user, password=config.password, database=config.dbname)
    cursor = mydb.cursor()
    
    select_query = """ SELECT * FROM expediente"""
    cursor.execute(select_query)
    records = cursor.fetchall()
    
    for row in records:
        name = row[1]
        diagnosis_ciphertext = row[2]
        treatment_ciphertext = row[3]
        passwordSalt = row[4]
        diagnosis_nonce = row[5]
        treatment_nonce = row[6]
        
        print(f"Name: {name}\nDiagnosis: {diagnosis_ciphertext}\nTreatment: {treatment_ciphertext}\n")
        
        passwordSalt = b64decode(passwordSalt)
        diagnosis_nonce = b64decode(diagnosis_nonce)
        treatment_nonce = b64decode(treatment_nonce)

        # Derivar la llave a partir de la contraseña y la salt
        key = PBKDF2(password, passwordSalt, dkLen=32, count=1000000)
        
        # Crear los objetos AES para descifrar
        diag_aes = AES.new(key,AES.MODE_GCM, nonce=diagnosis_nonce)
        treat_aes = AES.new(key, AES.MODE_GCM, nonce=treatment_nonce)
        
        diagnosis, treatment = descifrar(diagnosis_ciphertext, treatment_ciphertext, diag_aes, treat_aes)
        print(f"Name: {name}\nDiagnosis: {diagnosis}\nTreatment: {treatment}\n")
    return records


password = 'p7_aes'
records = consultar_pacientes(password)

    