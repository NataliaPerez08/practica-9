import base64
from getpass import getpass
from Cryptodome.Cipher import AES
from Cryptodome.Protocol.KDF import PBKDF2
from Cryptodome.Hash import SHA512
import MySQLdb, config, sys

def descifrar(diagnosis_ciphertext, treatment_ciphertext, password, passwordSalt, diagnosis_nonce, treatment_nonce):
    try:
        # Decodificar las cadenas de entrada
        passwordSalt = base64.b64decode(passwordSalt)
        diagnosis_ciphertext = base64.b64decode(diagnosis_ciphertext)
        treatment_ciphertext = base64.b64decode(treatment_ciphertext)
        diagnosis_nonce = base64.b64decode(diagnosis_nonce)
        treatment_nonce = base64.b64decode(treatment_nonce)

        # Derivar la clave de cifrado usando PBKDF2
        key = PBKDF2(password, passwordSalt, 32, count=1000000, hmac_hash_module=SHA512)

        # Crear objetos AES para descifrar usando el mismo nonce
        diag_aes = AES.new(key, AES.MODE_CTR, nonce=diagnosis_nonce)
        treat_aes = AES.new(key, AES.MODE_CTR, nonce=treatment_nonce)

        # Descifrar los textos cifrados
        diagnosis_decrypted = diag_aes.decrypt(diagnosis_ciphertext)
        treatment_decrypted = treat_aes.decrypt(treatment_ciphertext)

        try:
            # Intentar decodificar los datos descifrados como UTF-8
            diagnosis_decrypted_text = diagnosis_decrypted.decode('utf-8')
            treatment_decrypted_text = treatment_decrypted.decode('utf-8')
        except UnicodeDecodeError as e:
            print(f"Error al decodificar los datos descifrados: {e}")
            print("Datos descifrados (diagnosis):", diagnosis_decrypted.hex())
            print("Datos descifrados (treatment):", treatment_decrypted.hex())
            return None, None

        return diagnosis_decrypted_text, treatment_decrypted_text

    except Exception as e:
        print(f"Error general al descifrar los datos: {e}")
        return None, None

def consultar_paciente_por_nombre(nombre, password):
    try:
        mydb = MySQLdb.connect(user=config.user, password=config.password, database=config.dbname)
        cursor = mydb.cursor()

        select_query = """ SELECT * FROM expediente WHERE nombre = %s """
        cursor.execute(select_query, (nombre,))
        record = cursor.fetchone()

        if record:
            name = record[1]
            diagnosis_ciphertext = record[2]
            treatment_ciphertext = record[3]
            passwordSalt = record[4]
            diagnosis_nonce = record[5]
            treatment_nonce = record[6]

            diagnosis, treatment = descifrar(diagnosis_ciphertext, treatment_ciphertext, password, passwordSalt, diagnosis_nonce, treatment_nonce)
            print(f"Name: {name}\nDiagnosis: {diagnosis}\nTreatment: {treatment}\n")
        else:
            print(f"No se encontró ningún paciente con el nombre '{nombre}' en la base de datos.")

    except Exception as e:
        print(f"Error al consultar la base de datos: {e}")
        sys.exit()

    finally:
        if mydb:
            cursor.close()
            mydb.close()


def main():
    password = input("Introduce la contraseña: ")
    nombre_paciente = input("Introduce el nombre del paciente: ")
    consultar_paciente_por_nombre(nombre_paciente, password)

if __name__ == "__main__":
    main()

