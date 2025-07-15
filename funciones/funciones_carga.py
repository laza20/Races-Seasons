from bson import ObjectId
from bson.errors import InvalidId
from fastapi import HTTPException, status
from db.client import db_client
from typing import get_type_hints
from funciones import funciones_logicas
    
    
def cargar_uno(dato, base_de_datos, schema, validacion):
        coleccion = getattr(db_client, base_de_datos)
        dict_dato = dict(dato)
        if base_de_datos != "Sistema_de_puntuacion":
            dict_dato["tipo"] = base_de_datos
        validacion(dato, base_de_datos)
        if dict_dato["temporada"]:
            dict_dato["temporada"] = funciones_logicas.validate_object_id(dict_dato["temporada"])
        id = coleccion.insert_one(dict_dato).inserted_id
        new_formato = schema(coleccion.find_one({"_id":id}))
        return new_formato
    
def cargar_uno_temporada(dato, base_de_datos, schema, validacion, campo):
        coleccion = getattr(db_client, base_de_datos)
        dict_dato = dict(dato)
        if base_de_datos in ["Equipos_por_temporada", "Pilotos_por_temporada", "Circuitos_por_temporada"]:
            dict_dato = buscar_data(dict_dato, campo, base_de_datos)
        validacion(dato, base_de_datos)
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
        lista.append(dict_dato)
        
    resultado = coleccion.insert_many(lista)
    ids = resultado.inserted_ids
    documentos = coleccion.find({"_id":{"$in":ids}})
    return schema(documentos)

def cargar_muchos_temporada(datos, base_de_datos, schema, validacion, campo):
    coleccion = getattr(db_client, base_de_datos)
    lista = []
    validacion(datos, base_de_datos)
    for dato in datos:
        dict_dato = dict(dato)
        if base_de_datos in ["Equipos_por_temporada", "Pilotos_por_temporada", "Circuitos_por_temporada"]:
            dict_dato = buscar_data(dict_dato, campo, base_de_datos)
        dict_dato["tipo"] = base_de_datos
        lista.append(dict_dato)
        
    resultado = coleccion.insert_many(lista)
    ids = resultado.inserted_ids
    documentos = coleccion.find({"_id":{"$in":ids}})
    return schema(documentos)




def buscar_data(dict_dato, campo, base_de_datos):
    if base_de_datos == "Circuitos_por_temporada":
        dict_dato[campo] = dict_dato["circuito"]
    elif base_de_datos == "Equipos_por_temporada": 
        dict_dato[campo] = dict_dato["nombre_equipo"]
    elif base_de_datos == "Pilotos_por_temporada":
        dict_dato[campo] = dict_dato["piloto_participante"]
    
    if campo is None or campo not in dict_dato:
        raise HTTPException(status_code=400, detail="Falta el campo necesario para búsqueda de datos")

    valor = dict_dato[campo]
    condiciones = [{campo: {"$regex": f"^{valor}$", "$options": "i"}}]
    try:
        condiciones.append({"_id": ObjectId(valor)})
    except:
        pass  # No es un ObjectId, no agregamos esa condición

    if base_de_datos == "Equipos_por_temporada":
        resultado = db_client.Equipos.find_one({"$or": condiciones})
    elif base_de_datos == "Pilotos_por_temporada":
        resultado = db_client.Pilotos.find_one({"$or": condiciones})
    elif base_de_datos == "Circuitos_por_temporada":
        resultado = db_client.Circuitos.find_one({"$or": condiciones})
    else:
        raise HTTPException(status_code=409, detail="Base de datos inválida para carga de datos faltantes")

    return carga_datos_faltantes(resultado, base_de_datos, dict_dato, campo)

def carga_datos_faltantes(resultado, base_de_datos, dict_dato, valor):
    if not resultado:
        return {"error": "No se encontraron datos"}
    
    temporada_oid = ObjectId(dict_dato["temporada"])
    dato_oid = ObjectId(resultado["_id"])
    
    if base_de_datos == "Equipos_por_temporada":
        dict_dato["nombre_equipo"]       = dato_oid
        dict_dato["pais_equipo"]         = resultado["pais_equipo"]
        dict_dato["temporada"]           = temporada_oid 
    elif base_de_datos == "Pilotos_por_temporada":
        dict_dato["edad_piloto"]         = resultado["edad_piloto"]
        dict_dato["nacionalidad_piloto"] = resultado["nacionalidad_piloto"]
        dict_dato["piloto_participante"] = dato_oid
        dict_dato["temporada"]           = temporada_oid 
    elif base_de_datos == "Circuitos_por_temporada":
        
        dict_dato["circuito"]               = dato_oid
        dict_dato["temporada"]              = temporada_oid
        dict_dato["ciudad_circuito"]        = resultado["ciudad_circuito"]
        dict_dato["pais_circuito"]          = resultado["pais_circuito"]
        dict_dato["distancia_del_circuito"] = resultado["distancia_del_circuito"]
    
    return dict_dato