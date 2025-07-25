from db.client import db_client
from fastapi import HTTPException, status
from funciones import funciones_logicas
from validaciones_generales import validaciones_generales_dobles, validaciones_generales_simples

        
def validar_carga_sistema_de_puntuacion(datos, base_de_datos):
    if isinstance(datos, list) and len(datos) >= 2:
        puntos = set()
        for dato in datos:
            key = validar_carga_sistema_de_puntuacion_2(dato, base_de_datos)
            if key in puntos:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Sistema de puntos duplicado en la entrega")
            puntos.add(key)
    else:
    
        dato = datos if not isinstance(datos, list) else datos[0]
        key  = validar_carga_sistema_de_puntuacion_2(dato, base_de_datos)
        

def validar_carga_sistema_de_puntuacion_2(dato, base_de_datos):
    temporada_oid = funciones_logicas.validate_object_id(dato.temporada)
    key = (dato.posicion, dato.puntos, dato.tipo_carrera.capitalize(), dato.temporada)
    
    validaciones_generales_simples.validacion_simple_general_negativa("Temporadas", temporada_oid)
    

    if db_client.Sistema_de_puntuacion.find_one({"posicion": dato.posicion, "puntos": dato.puntos, "temporada":temporada_oid, "tipo_carrera": dato.tipo_carrera}):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Sistema de puntos ya ingresados en Base de datos")
    
    return key
        