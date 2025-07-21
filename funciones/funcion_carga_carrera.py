from db.client import db_client
from db.schemas.carreras import carrera_carga_schema, carrera_schema, carreras_carga_schema,carreras_schema
from db.schemas.puntos_por_piloto import puntos_por_piloto_schema, puntos_por_pilotos_schema
from db.schemas.puntos_por_equipos import puntos_por_equipo_schema,puntos_por_equipos_schema
from db.models.carrera_todos_los_datos import DatosTotales
from funciones import funciones_carga, funciones_logicas




async def cargar_carrera(dato, base_de_datos, schema, validacion):
    coleccion_carreras = getattr(db_client, base_de_datos)
    coleccion_pilotos = getattr(db_client, "Carreras_por_pilotos")
    coleccion_equipos = getattr(db_client, "Carreras_por_equipos")
    
    temporada_oid = funciones_logicas.validate_object_id(dato.temporada)
    
    lista_carrera = []
    lista_puntos_piloto  = []
    lista_puntos_equipo  = []
    
    
    puntos = buscar_puntos_por_posicion(dato, temporada_oid)
    
    dict_puntos_por_piloto =  logica_carga_piloto (dato, temporada_oid, puntos)
    dict_puntos_equipo     =  logica_carga_equipo (dato, temporada_oid, puntos)
    dict_carrera           =  logica_carga_carrera(dato, temporada_oid)
    
    validacion(dato, base_de_datos)
    
    
    id_piloto = coleccion_pilotos.insert_one(dict_puntos_por_piloto).inserted_id
    new_puntos_por_pilotos = puntos_por_piloto_schema(coleccion_pilotos.find_one({"_id":id_piloto}))
    

    id_equipo = coleccion_equipos.insert_one(dict_puntos_equipo).inserted_id
    new_puntos_por_equipos = puntos_por_equipo_schema(coleccion_equipos.find_one({"_id":id_equipo}))
    
    
    id_carrera  = coleccion_carreras.insert_one(dict_carrera).inserted_id
    new_carrera = carrera_schema(coleccion_carreras.find_one({"_id":id_carrera}))
    
    
    lista_carrera       = [new_carrera]
    lista_puntos_equipo = [new_puntos_por_equipos]
    lista_puntos_piloto = [new_puntos_por_pilotos] 
    

    return DatosTotales(
        carreras        = lista_carrera,
        puntos_x_equipo = lista_puntos_equipo,
        puntos_x_piloto = lista_puntos_piloto
    )
    
    
def buscar_puntos_por_posicion(carrera, temporada_oid):
    puntos_doc = db_client.Sistema_de_puntuacion.find_one({"posicion": carrera.posicion,"tipo_carrera":carrera.tipo_carrera, "temporada":temporada_oid})
    if puntos_doc:
        puntos = puntos_doc["puntos"]
    else:
        puntos = 0
    
    return puntos
    
def logica_carga_equipo(carrera, temporada_oid, puntos):
    filtro_equipo={
            "id"                  : "",
            "equipo_participante" : carrera.equipo_participante,
            "puntos_equipo"       : puntos,
            "ciudad_circuito"     : carrera.ciudad_circuito,
            "cant_dnf"            : carrera.dnf,
            "fecha"               : carrera.fecha,
            "temporada"           : temporada_oid,
            "tipo_carrera"        : carrera.tipo_carrera,
            "tipo"                : "Carreras_por_equipos",
            "estado"              : carrera.estado
        }
        
    dict_puntos_equipos              = dict(filtro_equipo)
    del dict_puntos_equipos["id"]
    dict_puntos_equipos["temporada"] = temporada_oid
    
    return dict_puntos_equipos

def logica_carga_piloto(carrera, temporada_oid, puntos):
    filtro_piloto={
            "id"                 : "",
            "piloto_participante": carrera.piloto_participante,
            "puntos_piloto"      : puntos,
            "ciudad_circuito"    : carrera.ciudad_circuito,
            "dnf"                : carrera.dnf,
            "fecha"              : carrera.fecha, 
            "temporada"          : temporada_oid,
            "tipo_carrera"        : carrera.tipo_carrera,
            "tipo"                : "Carreras_por_pilotos",
            "estado"             : carrera.estado
        }
    
    dict_puntos_por_pilotos              = dict(filtro_piloto)
    del dict_puntos_por_pilotos["id"]
    dict_puntos_por_pilotos["temporada"] = temporada_oid
    
    return dict_puntos_por_pilotos


def  logica_carga_carrera(carrera, temporada_oid):    
    dict_carrera              = dict(carrera)
    del dict_carrera["id"]    
    dict_carrera["fecha"]     = carrera.fecha
    dict_carrera["tipo"]      = "Carreras" 
    dict_carrera["temporada"] = temporada_oid
    
    return dict_carrera