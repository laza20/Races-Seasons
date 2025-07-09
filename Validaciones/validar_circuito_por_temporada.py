from db.client import db_client
from fastapi import HTTPException, status
from funciones import funciones_logicas

        
def validar_carga_circuito_por_temporada(datos, base_de_datos):
    coleccion = getattr(db_client, base_de_datos)
    if isinstance(datos, list) and len(datos) >= 2:
        circuitos = set()
        for dato in datos:
            key = validar_carga_circuito_por_temporada_2(dato, coleccion, datos)
            if key in circuitos:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Circuito duplicado en la entrega"
                )
            circuitos.add(key)
    else:
        dato = datos if not isinstance(datos, list) else datos[0]
        validar_carga_circuito_por_temporada_2(dato, coleccion, datos)

#Funcion para evitar la duplicidad de la carga de documentos de circuitos por temporada
def validar_carga_circuito_por_temporada_2(dato, coleccion, datos):
        temporada_oid = funciones_logicas.validate_object_id(dato.temporada)
        circuito_oid = funciones_logicas.validate_object_id_or_false(dato.circuito)
        circuito = db_client.Circuitos.find_one({"ciudad_circuito":dato.circuito})
        if not circuito and not circuito_oid:
            raise HTTPException(status_code=400, detail="Circuito no válido")
        
        if circuito:
            dict_circuito = dict(circuito)
            circuito_oid = funciones_logicas.validate_object_id(dict_circuito["_id"])
        key = (temporada_oid, circuito_oid)
            
        season = db_client.Temporadas.find_one({"_id": temporada_oid})
                    
        if not db_client.Temporadas.find_one({"_id": temporada_oid}):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Temporada incorrecta")
            
        if not db_client.Circuitos.find_one({"_id":circuito_oid}):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Circuito incorrecto (no encontrado en la base de datos)")
            
        if coleccion.find_one({"temporada": temporada_oid, "circuito":circuito_oid}):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Circuito ya ingresado en la temporada")
        
        limitacion_cantidad_por_temporada(season, temporada_oid, datos, coleccion)
        
        return key
        
def limitacion_cantidad_por_temporada(season, temporada_oid, datos, coleccion):
        cantidad_actual = coleccion.count_documents({"temporada": temporada_oid})
        
        cantidad_maxima = season.get("cantidad_de_grandes_premios")
        if not isinstance(cantidad_maxima, int):
            raise HTTPException(status_code=500, detail="El campo 'cantidad_de_grandes_premios' no está bien definido en la temporada")
        
        cantidad_nueva = len(datos) if isinstance(datos, list) else 1
        
        if cantidad_actual + cantidad_nueva > cantidad_maxima:
            raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"No se pueden agregar {cantidad_nueva} circuitos: la temporada ya tiene {cantidad_actual}/{cantidad_maxima}"
            )