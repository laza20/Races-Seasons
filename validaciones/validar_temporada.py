from fastapi import HTTPException, status
from db.client import db_client
from validaciones_generales import validaciones_generales_dobles
from funciones import funciones_logicas
        
        
def validar_carga_temporada(datos, base_de_datos):
    if isinstance(datos, list) and len(datos) >= 2:
        claves = set()
        for dato in datos:
            key, temporada  = validar_carga_temporada_2(dato, base_de_datos)
            verificar_entrega_duplicada(key, claves, temporada)
            claves.add(key)
    else:
        # Es un único circuito
        dato = datos if not isinstance(datos, list) else datos[0]
        key, temporada  = validar_carga_temporada_2(dato, base_de_datos)
        
def verificar_entrega_duplicada(key, puntos, temporada):
            if key in puntos:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"La temporada {temporada['descripcion']} fue ingresada dos veces en la entrega")
        
def validar_carga_temporada_2(dato, base_de_datos):
    temporada_oid = funciones_logicas.validate_object_id(dato.temporada)
    key = create_key(dato)
    validaciones_generales_dobles.validacion_doble_general(base_de_datos, dato.categoria, dato.year)
    season = buscar_temporada(temporada_oid)
    return key, season

def create_key(dato):
    key = (dato.year , dato.categoria.lower())
    return key

def buscar_temporada(temporada_oid):
    season = db_client.Temporadas.find_one({"_id":temporada_oid})
    return season