# Modulo que realiza la conexion a la base de datos y las operaciones de datos

import MySQLdb, config, sys

# Funcion que realiza la conexion a la base de datos
def conectar():
    try:
        # Leemos las credenciales para la conexión del archivo config.py
        # El cifrado de la conexión se realizará en otra práctica
        mydb = MySQLdb.connect(user=config.user, password=config.password, database=config.dbname)
        return mydb
    except Exception as err:
        print(f"\nSomething went wrong: {err}")
        sys.exit()
        
# Funcion que realiza inserciones en la base de datos
def insertar(mydb, name, diagnosis_ciphertext, treatment_ciphertext, passwordSalt, diagnosis_nonce, treatment_nonce):
    try:
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
        cursor.close()

