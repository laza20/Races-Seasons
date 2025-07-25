from db.client import db_client
from validaciones_generales.lista_de_campos import listas_de_campos
from errores import errores_simples

def validacion_simple_general(base_de_datos, dato):
    coleccion = getattr(db_client, base_de_datos)
    
    if base_de_datos not in listas_de_campos:
        errores_simples.error_sin_base_de_datos(base_de_datos)
    
    campos = listas_de_campos[base_de_datos]
    
    if isinstance(dato, str):
        validacion_simple_str(coleccion, campos, base_de_datos, dato)
    else:
        validacion_simple_no_str(coleccion, campos, base_de_datos, dato)


def validacion_simple_general_negativa(base_de_datos, dato):
    coleccion = getattr(db_client, base_de_datos)
    
    if base_de_datos not in listas_de_campos:
        errores_simples.error_sin_base_de_datos(base_de_datos)
    
    campos = listas_de_campos[base_de_datos]
    
    if isinstance(dato, str):
        validacion_simple_negativa_str(coleccion, campos, base_de_datos, dato)
    else:
        validacion_simple_negativa_no_str(coleccion, campos, base_de_datos, dato)


def validacion_simple_str(coleccion, campos, base_de_datos, dato):
    for campo in campos:
        query = {
            campo: {"$regex": f"^{dato}$", "$options": "i"}
             }
        if coleccion.find_one(query):
            errores_simples.error_simple_positivo(dato, base_de_datos, campo)
            
def validacion_simple_no_str(coleccion, campos, base_de_datos, dato):
    for campo in campos:
        query = {
            campo:dato
        }
        if coleccion.find_one(query):
            errores_simples.error_simple_positivo(dato, base_de_datos, campo)
        
        
def validacion_simple_negativa_str(coleccion, campos, base_de_datos, dato):
    for campo in campos:
        query = {
            campo: {"$regex": f"^{dato}$", "$options": "i"}
            }
        if coleccion.find_one(query):
            return
                
    errores_simples.error_simple_negativo(dato, base_de_datos)
                

def validacion_simple_negativa_no_str(coleccion, campos, base_de_datos, dato):
    for campo in campos:
        query = {
            campo: dato
            }
        if coleccion.find_one(query):
            return
                
    errores_simples.error_simple_negativo(dato, base_de_datos)
                
