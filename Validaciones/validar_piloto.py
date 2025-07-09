from db.client import db_client
from fastapi import HTTPException, status
from funciones import funciones_logicas


def validacion_carga_piloto(datos, base_de_datos):
    coleccion = getattr(db_client, base_de_datos)
    if isinstance(datos, list) and len(datos) >= 2:
        pilotos = set()
        for dato in datos:
            key = (dato.piloto_participante.lower(), dato.edad_piloto)
            
            if key in pilotos:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Mismo piloto ingresado 2 veces")
            pilotos.add(key)
            

            if coleccion.find_one({"piloto_participante": dato.piloto_participante, "edad_piloto": dato.edad_piloto}):
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"El piloto {dato.piloto_participante} ya está cargado")
    else:
        dato = datos if not isinstance(datos, list) else datos[0]

        if coleccion.find_one({"piloto_participante": dato.piloto_participante, "edad_piloto": dato.edad_piloto}):
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"El piloto {dato.piloto_participante} ya está cargado")
        