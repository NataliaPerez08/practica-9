
from base64 import b64encode

def cifrar(diagnosis, treatment, diag_aes, treat_aes):
    diagnosis = bytes(diagnosis, 'utf-8')
    treatment = bytes(treatment, 'utf-8')
    
    diagnosis_ciphertext = diag_aes.encrypt(diagnosis)
    treatment_ciphertext = treat_aes.encrypt(treatment)
    
    diagnosis_ciphertext = b64encode(diagnosis_ciphertext).decode('utf-8')
    treatment_ciphertext = b64encode(treatment_ciphertext).decode('utf-8')

    return diagnosis_ciphertext, treatment_ciphertext

