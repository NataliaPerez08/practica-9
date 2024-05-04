import json
import re

def lector(path:str):
    with open(path, 'r') as file:
        return file.read()
    
lectura = lector('ArchivosBase/diagnosticos_tratamientos.txt')
        
# Eliminar los corchetes del inicio y fin del string
string_sin_corchetes = lectura.strip('{}')

# Dividir el string en cada objeto utilizando expresiones regulares
objetos = re.split(r'\},\s*(?=\d+:)', string_sin_corchetes)

print(objetos[0:5])
