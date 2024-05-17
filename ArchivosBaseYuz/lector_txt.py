import json
import re

def lector(path:str)->str:
    with open(path, 'r') as file:
        return file.read()
    
def recuperar_pacientes()->list:  
    lectura = lector('./diagnosticos_tratamientos.txt')
    # Eliminar los corchetes del inicio y fin del string
    string_sin_corchetes = lectura.strip('{}')

    # Dividir el string en cada objeto utilizando expresiones regulares
    objetos = re.split(r'\},\s*(?=\d+:)', string_sin_corchetes)

    # Crear un diccionario con los objetos
    diccionario = {}
    for objeto in objetos:
        index = objeto.find(':')
        diccionario[objeto[:index]] = objeto[index+1:].strip('"')

    # Recorrer el diccionario y recuperar los atributos de cada objeto
    json_list = list()
    for key, value in diccionario.items():
        # Reemplazar comillas simples por comillas dobles
        value = value + "}"
        value = value.replace("'", '"')
        jo = json.loads(value)
        json_list.append(jo)
    return json_list 


