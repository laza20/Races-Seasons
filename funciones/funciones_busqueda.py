from db.client import db_client
from validaciones_generales.lista_de_campos import listas_de_campos
from errores import errores_simples
from funciones import funciones_logicas
from fastapi import HTTPException, status


def buscar_oid_con_dato(base_de_datos, dato):
    coleccion = getattr(db_client, base_de_datos)
    if base_de_datos not in listas_de_campos:
        errores_simples.error_sin_base_de_datos(base_de_datos)
        
    campos = listas_de_campos[base_de_datos]
    
    for campo in campos:
        resultado = coleccion.find_one({campo:dato})
        if resultado:
            resultado_oid = funciones_logicas.validate_object_id(resultado["_id"])
            return resultado_oid
        
    errores_simples.error_sin_oid(dato, base_de_datos)
    
    
def encontrar_un_dato(dato, base_de_datos):
    coleccion = getattr(db_client, base_de_datos)
    if base_de_datos not in listas_de_campos:
        errores_simples.error_sin_base_de_datos(base_de_datos)
        
    campos = listas_de_campos[base_de_datos]
    for campo in campos:
        resultado = coleccion.find_one({campo:dato})
        if resultado:
            return resultado
    
    errores_simples.error_sin_documentos_en_la_base_de_datos(dato, base_de_datos)
    