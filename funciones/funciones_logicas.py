from bson import ObjectId
from bson.errors import InvalidId
from fastapi import HTTPException, status
from db.client import db_client
from typing import get_type_hints
from db.schemas.temporada import temporada_schema


def validate_object_id(id: str):
    try:
        return ObjectId(id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="ID inválido")
    
def validate_object_id_or_false(id: str):
    try:
        return ObjectId(id)
    except InvalidId:
        return False
    
def identificar_temporada_por_year_y_categoria(year, categoria):
        temporada = temporada_schema(db_client.Temporadas.find_one({"year":year,"categoria":categoria}))
        if not temporada:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="temporada incorrecta")
        return temporada
    
def identificar_temporada_por_id(id):
    oid = validate_object_id_or_false(id)
    temporada = temporada_schema(db_client.Temporadas.find_one({"_id":oid}))
    if not temporada:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Temporada incorrecta")
    
    return temporada
    
def transformar_de_id_a_descripcion_o_nombre(id, base_de_datos,schema, base_de_datos_2):
    coleccion = getattr(db_client, base_de_datos)
    documento = coleccion.find_one({"_id": id})
    
    if not documento:
        return None 

    resultado = schema(documento)
    
    descripcion = resultado.get("descripcion") if isinstance(resultado, dict) else None

    if descripcion:
        return descripcion
    
    if isinstance(resultado, dict):
        valores = list(resultado.values())
    else:
        # Para objetos tipo Pydantic o clases normales
        valores = list(resultado.__dict__.values())
        
    busqueda = buscar_data(valores[1], base_de_datos_2)
    return list(busqueda.values())[1] if len(busqueda) >= 2 else list(busqueda.values())[0]

  
def buscar_data(id, base_de_datos_2):
    coleccion = getattr(db_client, base_de_datos_2)
    oid = validate_object_id(id)
    data = coleccion.find_one({"_id":oid})
    if not data:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Dato incorrecta")
    
    return data