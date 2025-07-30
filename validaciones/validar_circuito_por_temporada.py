from db.client import db_client
from fastapi import HTTPException, status
from funciones import funciones_logicas
from validaciones_generales import validaciones_generales_dobles, validaciones_generales_simples
from funciones import funciones_busqueda

        
def validar_carga_circuito_por_temporada(datos, base_de_datos):
    coleccion = getattr(db_client, base_de_datos)
    if isinstance(datos, list) and len(datos) >= 2:
        circuitos = set()
        for dato in datos:
            key = validar_carga_circuito_por_temporada_2(dato, coleccion, datos, base_de_datos)
            validar_carga_repetida(key, circuitos)
            circuitos.add(key)
    else:
        dato = datos if not isinstance(datos, list) else datos[0]
        key = validar_carga_circuito_por_temporada_2(dato, coleccion, datos, base_de_datos)

#Funcion para evitar la duplicidad de la carga de documentos de circuitos por temporada
def validar_carga_circuito_por_temporada_2(dato, coleccion, datos, base_de_datos):
        temporada_oid = funciones_logicas.validate_object_id(dato.temporada)
        circuito_oid = funciones_logicas.validate_object_id_or_false(dato.circuito)
        circuito, season = (dato, temporada_oid)
        verificar_existencia(dato, circuito, circuito_oid)
        transformar_circuito(circuito)
        key = (temporada_oid, circuito_oid)
        validaciones_simples(temporada_oid, circuito_oid)
        validaciones_generales_dobles.validacion_doble_general(base_de_datos, temporada_oid, circuito_oid )     
        limitacion_cantidad_por_temporada(season, temporada_oid, datos, coleccion)
        
        return key

def validar_carga_repetida(key, circuitos):
    if key in circuitos:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Circuito duplicado en la entrega"
        )
    
def transformar_circuito(circuito):
    if circuito:
        dict_circuito = dict(circuito)
        circuito_oid = funciones_logicas.validate_object_id(dict_circuito["_id"])
        return circuito_oid
    
def verificar_existencia(dato, circuito, circuito_oid):
    if not circuito and not circuito_oid:
        raise HTTPException(status_code=400, detail=f"Circuito {dato.circuito} no válido")
    
def encontrar_datos(dato, temporada_oid):
        circuito = funciones_busqueda.encontrar_un_dato(dato.circuito, "Circuitos")
        season   = funciones_busqueda.encontrar_un_dato(temporada_oid, "Temporadas") 
        return circuito, season
    
def validaciones_simples(temporada_oid, circuito_oid):
        validaciones_generales_simples.validacion_simple_general_negativa("Temporadas", temporada_oid)
        validaciones_generales_simples.validacion_simple_general_negativa("Circuitos", circuito_oid)
    
        
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