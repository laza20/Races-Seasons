from db.client import db_client
from fastapi import HTTPException, status
from funciones import funciones_logicas

        
def validar_carga_piloto_por_temporada(datos, base_de_datos):
    coleccion = getattr(db_client, base_de_datos)
    if isinstance(datos, list) and len(datos) >= 2:
        pilotos = set()
        for dato in datos:
            key = validar_carga_piloto_por_temporada_2(dato, coleccion)
            if key in pilotos:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="piloto duplicado en la entrega"
                )
            pilotos.add(key)
    else:
        dato = datos if not isinstance(datos, list) else datos[0]
        validar_carga_piloto_por_temporada_2(dato, coleccion)

#Funcion para evitar la duplicidad de la carga de documentos de pilotos por temporada
def validar_carga_piloto_por_temporada_2(dato, coleccion):
        temporada_oid = funciones_logicas.validate_object_id(dato.temporada)
        piloto_oid = funciones_logicas.validate_object_id_or_false(dato.piloto_participante)
        piloto = db_client.Pilotos.find_one({"piloto_participante":dato.piloto_participante})
        if not piloto and not piloto_oid:
            raise HTTPException(status_code=400, detail="Piloto no válido")
        
        if piloto:
            dict_piloto = dict(piloto)
            piloto_oid = funciones_logicas.validate_object_id(dict_piloto["_id"])
        key = (temporada_oid, piloto_oid)
                    
        if not db_client.Temporadas.find_one({"_id": temporada_oid}):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Temporada incorrecta")
            
        if not db_client.Pilotos.find_one({"_id":piloto_oid}):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Piloto incorrecto (no encontrado en la base de datos)")
            
        if coleccion.find_one({"temporada": temporada_oid, "piloto_participante":piloto_oid}):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Piloto ya ingresado en la temporada")
        
        return key
        
