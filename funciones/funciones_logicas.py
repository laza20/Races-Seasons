from bson import ObjectId
from bson.errors import InvalidId
from fastapi import HTTPException, status
from db.client import db_client
from typing import get_type_hints

def validate_object_id(id: str):
    try:
        return ObjectId(id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="ID inválido")
    
def cargar_uno(dato, base_de_datos, schema, validacion):
        coleccion = getattr(db_client, base_de_datos)
        validacion(dato, base_de_datos)
        dict_dato = dict(dato)
        dict_dato["tipo"] = base_de_datos
        id = coleccion.insert_one(dict_dato).inserted_id
        new_formato = schema(coleccion.find_one({"_id":id}))
        return new_formato
    
def cargar_muchos(datos, base_de_datos , schema, validacion):
    coleccion = getattr(db_client, base_de_datos)
    lista = []
    validacion(datos, base_de_datos)
    for dato in datos:
        dict_dato = dict(dato)
        if base_de_datos != "Sistema_de_puntuacion":
            dict_dato["tipo"] = base_de_datos
        else:
            continue
        lista.append(dict_dato)
        
    resultado = coleccion.insert_many(lista)
    ids = resultado.inserted_ids
    documentos = coleccion.find({"_id":{"$in":ids}})
    return schema(documentos)

#def buscar_data(input, campo, base_de_datos):
#    coleccion = getattr(db_client, base_de_datos)
#    condiciones = [{campo: {"$regex": f"^{input}$", "$options": "i"}}]
#    try:
#        condiciones.append({"_id": ObjectId(input)})
#    except:
#        pass  # No es un ObjectId, no agregamos esa condición

#    resultado = coleccion.find_one({"$or": condiciones})
#    return carga_datos_faltantes(resultado, coleccion)

#def carga_datos_faltantes(resultado, coleccion):
#    if not resultado:
#        return {"error": "No se encontraron datos"}
#    datos_completos = resultado.copy()
#    while True:
        