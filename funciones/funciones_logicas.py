from bson import ObjectId
from bson.errors import InvalidId
from fastapi import HTTPException, status
from db.client import db_client

def validate_object_id(id: str):
    try:
        return ObjectId(id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="ID inválido")
    
def cargar_uno(dato, base_de_datos, schema):
        coleccion = getattr(db_client, base_de_datos)
        dict_dato = dict(dato)
        dict_dato["tipo"] = base_de_datos
        id = coleccion.insert_one(dict_dato).inserted_id
        new_formato = schema(coleccion.find_one({"_id":id}))
        return new_formato
    
def cargar_muchos(datos, base_de_datos , schema, validacion):
    coleccion = getattr(db_client, base_de_datos)
    lista = []
    for dato in datos:
        validacion(dato, base_de_datos)
        dict_dato = dict(dato)
        dict_dato["tipo"] = base_de_datos
        lista.append(dict_dato)
        
    resultado = coleccion.insert_many(lista)
    ids = resultado.inserted_ids
    documentos = coleccion.find({"_id":{"$in":ids}})
    return schema(documentos)