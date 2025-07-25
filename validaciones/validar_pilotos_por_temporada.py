from db.client import db_client
from fastapi import HTTPException, status
from funciones import funciones_logicas
from validaciones_generales import validaciones_generales_simples, validaciones_generales_dobles

        
def validar_carga_piloto_por_temporada(datos, base_de_datos):
    if isinstance(datos, list) and len(datos) >= 2:
        pilotos = set()
        for dato in datos:
            key = validar_carga_piloto_por_temporada_2(dato, base_de_datos)
            if key in pilotos:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="piloto duplicado en la entrega"
                )
            pilotos.add(key)
    else:
        dato = datos if not isinstance(datos, list) else datos[0]
        validar_carga_piloto_por_temporada_2(dato, base_de_datos)

#Funcion para evitar la duplicidad de la carga de documentos de pilotos por temporada
def validar_carga_piloto_por_temporada_2(dato, base_de_datos):
        temporada_oid = funciones_logicas.validate_object_id(dato.temporada)
        piloto_oid    = funciones_logicas.validate_object_id_or_false(dato.piloto_participante)
        piloto        = db_client.Pilotos.find_one({"piloto_participante":dato.piloto_participante})
        
        if not piloto and not piloto_oid:
            raise HTTPException(status_code=400, detail="Piloto no válido")
        
        if piloto:
            dict_piloto = dict(piloto)
            piloto_oid = funciones_logicas.validate_object_id(dict_piloto["_id"])
        key = (temporada_oid, piloto_oid)
                    
        validaciones_generales_simples.validacion_simple_general_negativa("Temporadas", temporada_oid)
        
        validaciones_generales_simples.validacion_simple_general_negativa("Pilotos", piloto_oid)
        
        validaciones_generales_dobles.validacion_doble_general(base_de_datos, temporada_oid, piloto_oid)

        return key
        
