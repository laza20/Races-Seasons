from db.client import db_client
from fastapi import HTTPException, status
from funciones import funciones_logicas

        
def validar_carga_equipo_por_temporada(datos, base_de_datos):
    coleccion = getattr(db_client, base_de_datos)
    if isinstance(datos, list) and len(datos) >= 2:
        equipos = set()
        for dato in datos:
            key = validar_carga_equipo_por_temporada_2(dato, coleccion, datos)
            if key in equipos:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Equipo duplicado en la entrega"
                )
            equipos.add(key)
    else:
        dato = datos if not isinstance(datos, list) else datos[0]
        validar_carga_equipo_por_temporada_2(dato, coleccion, datos)

#Funcion para evitar la duplicidad de la carga de documentos de Equipos por temporada
def validar_carga_equipo_por_temporada_2(dato, coleccion, datos):
        temporada_oid = funciones_logicas.validate_object_id(dato.temporada)
        equipo_oid = funciones_logicas.validate_object_id_or_false(dato.nombre_equipo)
        equipo = db_client.Equipos.find_one({"nombre_equipo":dato.nombre_equipo})
        if not equipo and not equipo_oid:
            raise HTTPException(status_code=400, detail="Equipo no válido")
        
        if equipo:
            dict_equipo = dict(equipo)
            equipo_oid = funciones_logicas.validate_object_id(dict_equipo["_id"])
        key = (temporada_oid, equipo_oid)
            
        season = db_client.Temporadas.find_one({"_id": temporada_oid})
                    
        if not db_client.Temporadas.find_one({"_id": temporada_oid}):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Temporada incorrecta")
            
        if not db_client.Equipos.find_one({"_id":equipo_oid}):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Equipo incorrecto (no encontrado en la base de datos)")
            
        if coleccion.find_one({"temporada": temporada_oid, "nombre_equipo":equipo_oid}):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Equipo ya ingresado en la temporada")
        
        limitacion_cantidad_por_temporada(season, temporada_oid, datos, coleccion)
        
        return key
        
def limitacion_cantidad_por_temporada(season, temporada_oid, datos, coleccion):
        cantidad_actual = coleccion.count_documents({"temporada": temporada_oid})
        
        cantidad_maxima = season.get("cantidad_de_equipos")
        if not isinstance(cantidad_maxima, int):
            raise HTTPException(status_code=500, detail="El campo 'cantidad_de_equipos' no está bien definido en la temporada")
            
        cantidad_nueva = len(datos) if isinstance(datos, list) else 1
        
        if cantidad_actual + cantidad_nueva > cantidad_maxima:
            raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"No se pueden agregar {cantidad_nueva} equipos: la temporada ya tiene {cantidad_actual}/{cantidad_maxima}"
            )