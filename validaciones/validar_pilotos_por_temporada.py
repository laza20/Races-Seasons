from db.client import db_client
from fastapi import HTTPException, status
from funciones import funciones_logicas
from validaciones_generales import validaciones_generales_simples, validaciones_generales_dobles

        
def validar_carga_piloto_por_temporada(datos, base_de_datos):
    if isinstance(datos, list) and len(datos) >= 2:
        pilotos = set()
        for dato in datos:
            key = validar_carga_piloto_por_temporada_2(dato, base_de_datos)
            verificar_entrega_duplicada(dato, key, pilotos)
            pilotos.add(key)
    else:
        dato = datos if not isinstance(datos, list) else datos[0]
        validar_carga_piloto_por_temporada_2(dato, base_de_datos)


def verificar_entrega_duplicada(dato, key, pilotos):
    if key in pilotos:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"el piloto = {dato.piloto_participante} duplicado en la entrega"
        )

#Funcion para evitar la duplicidad de la carga de documentos de pilotos por temporada
def validar_carga_piloto_por_temporada_2(dato, base_de_datos):
    temporada_oid, piloto_oid = buscar_oids(dato)
    piloto = buscar_data(dato)
    validar_piloto(piloto, piloto_oid)
    key = create_key(piloto, temporada_oid)
    validaciones_simples(temporada_oid, piloto_oid)
    validaciones_generales_dobles.validacion_doble_general(base_de_datos, temporada_oid, piloto_oid)
    return key

def create_key(piloto, temporada_oid):
    if piloto:
        dict_piloto = dict(piloto)
        piloto_oid = funciones_logicas.validate_object_id(dict_piloto["_id"])
    key = (temporada_oid, piloto_oid)
    return key

def validar_piloto(piloto, piloto_oid):
    if not piloto and not piloto_oid:
        raise HTTPException(status_code=400, detail="Piloto no válido")

def buscar_data(dato):
    piloto  = db_client.Pilotos.find_one({"piloto_participante":dato.piloto_participante})
    return piloto

def buscar_oids(dato):
        temporada_oid = funciones_logicas.validate_object_id(dato.temporada)
        piloto_oid    = funciones_logicas.validate_object_id_or_false(dato.piloto_participante)
        return temporada_oid, piloto_oid
        
def validaciones_simples(temporada_oid, piloto_oid):
        validaciones_generales_simples.validacion_simple_general_negativa("Temporadas", temporada_oid)
        validaciones_generales_simples.validacion_simple_general_negativa("Pilotos", piloto_oid)
