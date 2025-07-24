from db.client import db_client
from fastapi import HTTPException, status
from funciones import funciones_logicas
        
        
listas_de_campos = {
    "Circuitos": ["_id", "ciudad_circuito", "pais_circuito", "distancia_del_circuito", "sistema_medicion", "tipo", "estado"],
    "Conformacion_de_equipos": ["_id", "nombre_equipo", "primer_piloto", "segundo_piloto", "piloto_reserva", "otro_piloto", "otro_piloto_dos", "temporada", "tipo", "estado"],
    "Equipos": ["_id", "nombre_equipo", "pais_equipo", "tipo", "estado"],
    "Circuitos_por_temporada": ["_id", "circuito", "ciudad_circuito", "pais_circuito", "distancia_del_circuito", "temporada", "tipo", "estado"],
    "Equipos_por_temporada": ["_id", "nombre_equipo", "pais_equipo", "equipo_actual", "temporada", "tipo", "estado"],
    "Pilotos_por_temporada": ["_id", "piloto_participante", "edad_piloto", "nacionalidad_piloto", "temporada", "tipo", "estado"],
    "PuntosPorPosicionCarrera": ["_id", "posicion", "puntos", "temporada", "tipo", "tipo_carrera", "estado"],
    "Temporadas": ["_id", "descripcion", "cantidad_de_grandes_premios", "cantidad_de_equipos", "observaciones", "tipo", "year", "categoria", "estado"],
    "Piloto": ["_id", "piloto_participante", "edad_piloto", "nacionalidad_piloto", "tipo", "estado"]
}

def validacion_simple(base_de_datos, dato):
    coleccion = getattr(db_client, base_de_datos)
    
    if base_de_datos not in listas_de_campos:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"No hay definición de campos para la colección {base_de_datos}")
    
    campos = listas_de_campos[base_de_datos]
    
    for campo in campos:
        query = (
            {campo: {"$regex": f"^{dato}$", "$options": "i"}} if isinstance(dato, str)
            else {campo: dato}
        )
        if coleccion.find_one(query):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"El dato '{dato}' ya se encuentra en la base de datos '{base_de_datos}' en el campo '{campo}'"
            )
        
        
def validacion_simple_negativa(base_de_datos, dato):
    coleccion = getattr(db_client, base_de_datos)
    
    if base_de_datos not in listas_de_campos:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"No hay definición de campos para la colección {base_de_datos}")
    
    campos = listas_de_campos[base_de_datos]
    
    for campo in campos:
        query = (
            {campo: {"$regex": f"^{dato}$", "$options": "i"}} if isinstance(dato, str)
            else {campo: dato}
        )
        if coleccion.find_one(query):
            return
        
        raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"El dato '{dato}' no se encuentra en la base de datos '{base_de_datos}'"
            )



def validacion_doble(base_de_datos, dato_uno, dato_dos):
    coleccion = getattr(db_client, base_de_datos)
    
    if base_de_datos not in listas_de_campos:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"No hay definición de campos para la colección {base_de_datos}")

    campos = listas_de_campos[base_de_datos]
    
    for i,campo_uno in enumerate(campos):
        for j,campo_dos in enumerate(campos):
            if i == j:
                continue
            
            query_1 = (
            {campo_uno: {"$regex": f"^{dato_uno}$", "$options": "i"}} if isinstance(dato_uno, str)
            else {campo_uno: dato_uno}
            )
            query_2 = (
            {campo_dos: {"$regex": f"^{dato_dos}$", "$options": "i"}} if isinstance(dato_dos, str)
            else {campo_dos: dato_dos}
            )
            if coleccion.find_one({**query_1, **query_2}):
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"El documento con los datos ({dato_uno} y {dato_dos}) ya se encuentra en la base de datos de {base_de_datos}")