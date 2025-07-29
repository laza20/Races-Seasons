from bson import ObjectId
from fastapi import HTTPException, status
from db.client import db_client
from funciones import funciones_logicas
    
#Funcion para agrupar el codigo repetido, permite cumplir con una responsabilidad unica por funcion. Armar el dict.    
def logica_de_carga_normal(dato, base_de_datos):
        dict_dato = dict(dato)
        dict_dato["tipo"] = base_de_datos
        if dict_dato.get("temporada", "") != "":
            dict_dato["temporada"] = funciones_logicas.validate_object_id(dict_dato["temporada"])
        
        return dict_dato

#Funcion para cargar un solo documento que no sean circuito_por_temporada, piloto_por_temporada, Equipo_por_temporada.
def cargar_uno(dato, base_de_datos, schema, validacion):
        coleccion = getattr(db_client, base_de_datos)
        validacion(dato, base_de_datos)
        dict_dato = logica_de_carga_normal(dato, base_de_datos)
        id = coleccion.insert_one(dict_dato).inserted_id
        new_formato = schema(coleccion.find_one({"_id":id}))
        return new_formato
    
#Funcion para cargar un muchos documentos que no sean circuito_por_temporada, piloto_por_temporada, Equipo_por_temporada.
def cargar_muchos(datos, base_de_datos , schema, validacion):
    coleccion = getattr(db_client, base_de_datos)
    lista = []
    validacion(datos, base_de_datos)
    for dato in datos:
        dict_dato = logica_de_carga_normal(dato, base_de_datos)
        lista.append(dict_dato)
        
    resultado = coleccion.insert_many(lista)
    ids = resultado.inserted_ids
    documentos = coleccion.find({"_id":{"$in":ids}})
    return schema(documentos)    

#Funcion para agrupar el codigo repetido, permite cumplir con una responsabilidad unica por funcion. Armar el dict.    
def logica_de_carga_normal_temporada(dato, base_de_datos, campo):
        dict_dato = dict(dato)
        if base_de_datos in ["Equipos_por_temporada", "Pilotos_por_temporada", "Circuitos_por_temporada"]:
            dict_dato = buscar_data(dict_dato, campo, base_de_datos)
        if dict_dato.get("temporada", "") != "":
            dict_dato["temporada"] = funciones_logicas.validate_object_id(dict_dato["temporada"])
        dict_dato["tipo"] = base_de_datos
        return dict_dato
    
#Funcion para cargar un solo documento que sea circuito_por_temporada, piloto_por_temporada, Equipo_por_temporada.    
def cargar_uno_temporada(dato, base_de_datos, schema, validacion, campo):
        coleccion = getattr(db_client, base_de_datos)
        validacion(dato, base_de_datos)
        dict_dato = logica_de_carga_normal_temporada(dato, base_de_datos, campo)
        id = coleccion.insert_one(dict_dato).inserted_id
        new_formato = schema(coleccion.find_one({"_id":id}))
        return new_formato
    
#Funcion para cargar un muchos documentos que sean circuito_por_temporada, piloto_por_temporada, Equipo_por_temporada.
def cargar_muchos_temporada(datos, base_de_datos, schema, validacion, campo):
    coleccion = getattr(db_client, base_de_datos)
    lista = []
    validacion(datos, base_de_datos)
    for dato in datos:
        dict_dato = logica_de_carga_normal_temporada(dato, base_de_datos, campo)
        lista.append(dict_dato)
        
    resultado = coleccion.insert_many(lista)
    ids = resultado.inserted_ids
    documentos = coleccion.find({"_id":{"$in":ids}})
    return schema(documentos)



#Funcion que permite buscar datos de la segunda base de datos, a que nos referimos, por ejemplo en circuitos por temporada
#es una categoria que parte de circuitos, por ende el usuario no debera ingresar todos los datos, solo con algunos
#sera interpretado por el programa y completara los restantes, esta funcion se encarga de esto.
def buscar_data(dict_dato, campo, base_de_datos):
    if base_de_datos == "Circuitos_por_temporada":
        dict_dato[campo] = dict_dato["circuito"]
    elif base_de_datos == "Equipos_por_temporada": 
        dict_dato[campo] = dict_dato["nombre_equipo"]
    elif base_de_datos == "Pilotos_por_temporada":
        dict_dato[campo] = dict_dato["piloto_participante"]
    
    if campo is None or campo not in dict_dato:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Falta el campo necesario para búsqueda de datos")

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
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Base de datos inválida para carga de datos faltantes")

    return carga_datos_faltantes(resultado, base_de_datos, dict_dato, campo)


#Se encarga de armar el diccionario final el cual contendra datos externo al json enviado por el usuario.
def carga_datos_faltantes(resultado, base_de_datos, dict_dato, valor):
    if not resultado:
        return {"error": "No se encontraron datos"}
    
    temporada_oid = funciones_logicas.validate_object_id(dict_dato["temporada"])
    dato_oid = ObjectId(resultado["_id"])
    
    if base_de_datos == "Equipos_por_temporada":
        dict_dato = equipos_por_temporada(dict_dato, resultado, dato_oid, temporada_oid)
    elif base_de_datos == "Pilotos_por_temporada":
        dict_dato = pilotos_por_temporada(dict_dato, resultado, dato_oid, temporada_oid)
    elif base_de_datos == "Circuitos_por_temporada":
        dict_dato = circuitos_por_temporada(dict_dato, resultado, dato_oid, temporada_oid)
            
    return dict_dato


#Arma el dict con los datos faltantes en caso de hablar de equipos_por_temporada
def equipos_por_temporada(dict_dato, resultado, dato_oid, temporada_oid):
    dict_dato["nombre_equipo"]       = dato_oid
    dict_dato["pais_equipo"]         = resultado["pais_equipo"]
    dict_dato["temporada"]           = temporada_oid 
    
    return dict_dato

#Arma el dict con los datos faltantes en caso de hablar de pilotos_por_temporada
def pilotos_por_temporada(dict_dato, resultado, dato_oid, temporada_oid):
    dict_dato["edad_piloto"]         = resultado["edad_piloto"]
    dict_dato["nacionalidad_piloto"] = resultado["nacionalidad_piloto"]
    dict_dato["piloto_participante"] = dato_oid
    dict_dato["temporada"]           = temporada_oid 
    
    return dict_dato

#Arma el dict con los datos faltantes en caso de hablar de circuitos_por_temporada
def circuitos_por_temporada(dict_dato, resultado, dato_oid, temporada_oid):
    dict_dato["circuito"]               = dato_oid
    dict_dato["temporada"]              = temporada_oid
    dict_dato["ciudad_circuito"]        = resultado["ciudad_circuito"]
    dict_dato["pais_circuito"]          = resultado["pais_circuito"]
    dict_dato["distancia_del_circuito"] = resultado["distancia_del_circuito"]
    
    return dict_dato