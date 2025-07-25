from db.client import db_client
from fastapi import HTTPException, status
from funciones import funciones_logicas
from validaciones_generales import validaciones_generales_dobles, validaciones_generales_simples

        
def validar_carga_equipo_por_temporada(datos, base_de_datos):
    if isinstance(datos, list) and len(datos) >= 2:
        equipos = set()
        for dato in datos:
            key = validar_carga_equipo_por_temporada_2(dato, base_de_datos, datos)
            if key in equipos:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Equipo duplicado en la entrega"
                )
            equipos.add(key)
    else:
        dato = datos if not isinstance(datos, list) else datos[0]
        validar_carga_equipo_por_temporada_2(dato, base_de_datos, datos)

#Funcion para evitar la duplicidad de la carga de documentos de Equipos por temporada
def validar_carga_equipo_por_temporada_2(dato, base_de_datos, datos):
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
        
        validaciones_generales_simples.validacion_simple_general_negativa("Temporadas", temporada_oid)
        validaciones_generales_simples.validacion_simple_general_negativa("Equipos", equipo_oid)
        validaciones_generales_dobles.validacion_doble_general(base_de_datos, temporada_oid, equipo_oid)
        
        limitacion_cantidad_por_temporada(season, temporada_oid, datos, base_de_datos)
        
        return key
        
def limitacion_cantidad_por_temporada(season, temporada_oid, datos, base_de_datos):
        coleccion = getattr(db_client, base_de_datos)
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