
from base64 import b64encode
# Este modulo se encargargar de cifrar los datos de los pacientes 
def cifrar(diagnosis, treatment, diag_aes, treat_aes):
    # Pasamos a bytes
    diagnosis = bytes(diagnosis, 'utf-8')
    treatment = bytes(treatment, 'utf-8')
    
    # Cifrado de los campos considerados sensibles
    diagnosis_ciphertext = diag_aes.encrypt(diagnosis)
    treatment_ciphertext = treat_aes.encrypt(treatment)
    
    return diagnosis_ciphertext, treatment_ciphertext