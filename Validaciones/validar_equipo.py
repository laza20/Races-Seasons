from db.client import db_client
from fastapi import HTTPException, status


def validacion_carga_equipo(datos, base_de_datos):
    coleccion = getattr(db_client, base_de_datos)
    if isinstance(datos, list) and len(datos) >= 2:
        equipos = set()
        for dato in datos:
            key = (dato.nombre_equipo.lower(), dato.pais_equipo.lower())
            
            if key in equipos:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Mismo Equipo ingresado 2 veces")
            equipos.add(key)
            
            if coleccion.find_one({"nombre_equipo": dato.nombre_equipo, "pais_equipo": dato.pais_equipo}):
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"El Equipo {dato.nombre_equipo} ya está cargado")
    else:
        dato = datos if not isinstance(datos, list) else datos[0]

        if coleccion.find_one({"nombre_equipo": dato.nombre_equipo, "pais_equipo": dato.pais_equipo}):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"El Equipo {dato.nombre_equipo} ya está cargado")
        