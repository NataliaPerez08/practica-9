# Modulo que se encarga de descifrar los datos de los pacientes

from base64 import b64decode
from Crypto.Cipher import AES
    
def descifrar(diagnosis_ciphertext, treatment_ciphertext, diag_aes, treat_aes):
    # Decodificar el cifrado
    diagnosis_ciphertext = b64decode(diagnosis_ciphertext)
    treatment_ciphertext = b64decode(treatment_ciphertext)
    
    # Descifrar los campos considerados sensibles
    diagnosis = diag_aes.decrypt(diagnosis_ciphertext)
    treatment = treat_aes.decrypt(treatment_ciphertext)
    
    return diagnosis, treatment

def consultar_pacientes(cursor, diag_aes, treat_aes):
    select_query = """ SELECT * FROM expediente"""
    cursor.execute(select_query)
    records = cursor.fetchall()
    
    for row in records:
        name = row[0]
        diagnosis_ciphertext = row[1]
        treatment_ciphertext = row[2]
        
        diagnosis, treatment = descifrar(diagnosis_ciphertext, treatment_ciphertext, diag_aes, treat_aes)
        print(f"Name: {name}, Diagnosis: {diagnosis}, Treatment: {treatment}")
        
    return records