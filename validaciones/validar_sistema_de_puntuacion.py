from db.client import db_client
from fastapi import HTTPException, status
from funciones import funciones_logicas

        
def validar_carga_sistema_de_puntuacion(datos, base_de_datos):
    if isinstance(datos, list) and len(datos) >= 2:
        puntos = set()
        for dato in datos:
            key = validar_carga_sistema_de_puntuacion_2(dato)
            if key in puntos:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Sistema de puntos duplicado en la entrega")
            puntos.add(key)
    else:
    
        dato = datos if not isinstance(datos, list) else datos[0]
        key  = validar_carga_sistema_de_puntuacion_2(dato)
        

def validar_carga_sistema_de_puntuacion_2(dato):
    temporada_oid = funciones_logicas.validate_object_id(dato.temporada)
    key = (dato.posicion, dato.puntos, dato.tipo_carrera.capitalize(), dato.temporada)
    if not db_client.Temporadas.find_one({"_id": temporada_oid}):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Temporada incorrecta")

    if db_client.Sistema_de_puntuacion.find_one({"posicion": dato.posicion, "puntos": dato.puntos, "temporada":temporada_oid, "tipo_carrera": dato.tipo_carrera}):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Sistema de puntos ya ingresados en Base de datos")
    
    return key
        