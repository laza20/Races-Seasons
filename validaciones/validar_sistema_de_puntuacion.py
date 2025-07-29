from db.client import db_client
from fastapi import HTTPException, status
from funciones import funciones_logicas
from validaciones_generales import validaciones_generales_simples

        
def validar_carga_sistema_de_puntuacion(datos):
    if isinstance(datos, list) and len(datos) >= 2:
        puntos = set()
        for dato in datos:
            key, temporada = validar_carga_sistema_de_puntuacion_2(dato)
            verificar_entrega_duplicada(dato, key, puntos, temporada)
            puntos.add(key)
    else:
    
        dato = datos if not isinstance(datos, list) else datos[0]
        key  = validar_carga_sistema_de_puntuacion_2(dato)
        

def verificar_entrega_duplicada(dato, key, puntos, temporada):
            if key in puntos:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Esta sistema de puntos = (posicion = '{dato.posicion}', puntos = '{dato.puntos}', tipo de carrera = {dato.tipo_carrera}) esta repetido en la entrega para la temporada = '{temporada['descripcion']}'")

def validar_carga_sistema_de_puntuacion_2(dato):
    temporada_oid = funciones_logicas.validate_object_id(dato.temporada)
    
    key = create_key(dato)
    season = buscar_data(temporada_oid)
    validaciones_generales_simples.validacion_simple_general_negativa("Temporadas", temporada_oid)
    validacion_sistema_de_puntuacion(dato, temporada_oid, season)

    return key, season

def create_key(dato):
    key = (dato.posicion, dato.puntos, dato.tipo_carrera.capitalize(), dato.temporada)
    return key

def buscar_data(temporada_oid):
    season = db_client.Temporadas.find_one({"_id":temporada_oid})
    return season

def validacion_sistema_de_puntuacion(dato, temporada_oid, season):
    if db_client.Sistema_de_puntuacion.find_one({"posicion": dato.posicion, "puntos": dato.puntos, "temporada":temporada_oid, "tipo_carrera": dato.tipo_carrera}):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Esta sistema de puntos = (posicion = '{dato.posicion}', puntos = '{dato.puntos}', tipo de carrera = {dato.tipo_carrera}) ya se encuentra en la base de datos para la temporada = '{season['descripcion']}'")
    