from db.client import db_client
from fastapi import HTTPException, status


def validacion_carga_equipo(datos, base_de_datos):
    if isinstance(datos, list) and len(datos) >= 2:
        equipos = set()
        for dato in datos:
            
            key = validacion_carga_equipo_2(dato)
            
            if key in equipos:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Mismo Equipo ingresado 2 veces")
            equipos.add(key)
    else:
        dato = datos if not isinstance(datos, list) else datos[0]
        key = validacion_carga_equipo_2(dato)
        
def validacion_carga_equipo_2(dato):
    key = (dato.nombre_equipo.lower(), dato.pais_equipo.lower())
    
    if db_client.Equipos.find_one({"nombre_equipo":{"$regex": f"^{dato.nombre_equipo}$", "$options": "i"}, "pais_equipo": {"$regex": f"^{dato.pais_equipo}$", "$options": "i"}}):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"El Equipo {dato.nombre_equipo} ya está cargado")
    
    return key
        