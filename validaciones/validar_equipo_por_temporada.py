from db.client import db_client
from fastapi import HTTPException, status
from funciones import funciones_logicas
from validaciones_generales import validaciones_generales_dobles, validaciones_generales_simples
from funciones import funciones_busqueda
        
def validar_carga_equipo_por_temporada(datos, base_de_datos):
    if isinstance(datos, list) and len(datos) >= 2:
        equipos = set()
        for dato in datos:
            key = validar_carga_equipo_por_temporada_2(dato, base_de_datos, datos)
            validar_carga_repetida(key, equipos, dato)
            equipos.add(key)
    else:
        dato = datos if not isinstance(datos, list) else datos[0]
        key = validar_carga_equipo_por_temporada_2(dato, base_de_datos, datos)


def validar_carga_repetida(key, equipos, dato):
    if key in equipos:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Equipo {dato.nombre_equipo} duplicado en la entrega"
        )
#Funcion para evitar la duplicidad de la carga de documentos de Equipos por temporada
def validar_carga_equipo_por_temporada_2(dato, base_de_datos, datos):
    equipo_oid, temporada_oid = buscar_oid(dato)
    equipo, season = buscar_data(dato, temporada_oid)
    verificar_data(equipo, equipo_oid)
    key = transformar_data(equipo, temporada_oid)
    validaciones_simples(temporada_oid, equipo_oid)
    validaciones_generales_dobles.validacion_doble_general(base_de_datos, temporada_oid, equipo_oid)
    
    limitacion_cantidad_por_temporada(season, temporada_oid, datos, base_de_datos)
    
    return key

def validaciones_simples(temporada_oid, equipo_oid):
    validaciones_generales_simples.validacion_simple_general_negativa("Temporadas", temporada_oid)
    validaciones_generales_simples.validacion_simple_general_negativa("Equipos", equipo_oid)

def transformar_data(equipo, temporada_oid):
    if equipo:
        dict_equipo = dict(equipo)
        equipo_oid = funciones_logicas.validate_object_id(dict_equipo["_id"])
        return (temporada_oid, equipo_oid)
    raise HTTPException(status_code=400, detail="Equipo inválido para transformar")


def verificar_data(equipo, equipo_oid):
    if not equipo and not equipo_oid:
        raise HTTPException(status_code=400, detail="Equipo no válido")

def buscar_data(dato, temporada_oid):
    equipo = funciones_busqueda.encontrar_un_documento(dato.nombre_equipo, "Equipos")
    season = funciones_busqueda.encontrar_un_documento(temporada_oid, "Temporadas")
    return equipo, season
    
def buscar_oid(dato):
    temporada_oid = funciones_logicas.validate_object_id(dato.temporada)
    equipo_oid = funciones_logicas.validate_object_id_or_false(dato.nombre_equipo)
    return equipo_oid, temporada_oid
        
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
            detail=f"Solo se pueden agregar {cantidad_maxima - cantidad_actual} equipos: temporada ya tiene {cantidad_actual}/{cantidad_maxima}"
            )