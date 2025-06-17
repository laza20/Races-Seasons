from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from db.models.sistema_de_puntuacion import PuntosPorPosicionCarrera , PuntosPorPosicionCarreraCarga
from db.client import db_client
from db.schemas.sistema_de_puntuacion import punto_schema, puntos_schema
from bson import ObjectId
from bson.errors import InvalidId

router = APIRouter(prefix="/Sistema/Puntuacion",
                   tags=["Sistema de puntuacion"], 
                   responses={404:{ "message":"No encontrado"}})

def validate_object_id(id: str):
    try:
        return ObjectId(id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="ID inválido")

@router.get("/", response_model=list[PuntosPorPosicionCarrera])
async def show_puntos():
    return puntos_schema(db_client.sistema_de_puntuacion.find())

@router.get("/Ver/{id}")
async def show_puntos_by_id(id:str):
    try:
        object_id = validate_object_id(id)
        return punto_schema(db_client.puntosxposicion.find_one({"_id":object_id}))
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID sin puntos")
    
@router.get("/Ver/Datos/Temporada/{temporada}", response_model=list[PuntosPorPosicionCarrera])
async def show_pilotos_by_category (temporada:str):
    objeto_id = validate_object_id(temporada)
    datas = puntos_schema(db_client.sistema_de_puntuacion.find({"temporada":objeto_id}))
    for data in datas:  
        temporada_oid     = ObjectId(data["temporada"])
        temporada = db_client.temporadas.find_one({"_id":temporada_oid})
        data["temporada"] = temporada["descripcion"] if temporada else "Desconocida"
        
    return datas 
    
@router.get("/Ver/Datos/Carga/{temporada}", response_model=list[PuntosPorPosicionCarreraCarga])
async def show_pilotos_by_category (temporada:str):
    objeto_id = validate_object_id(temporada)
    datas = puntos_schema(db_client.sistema_de_puntuacion.find({"temporada":objeto_id}))
    return datas

@router.get("/Ver/Datos/Temporada/Tipo/{temporada}/{tipo}", response_model=list[PuntosPorPosicionCarrera])
async def show_pilotos_by_category (temporada:str, tipo:str):
    objeto_id = validate_object_id(temporada)
    datas = puntos_schema(db_client.sistema_de_puntuacion.find({"temporada":objeto_id, "tipo":tipo}))
    for data in datas:  
        temporada_oid     = ObjectId(data["temporada"])
        temporada = db_client.temporadas.find_one({"_id":temporada_oid})
        data["temporada"] = temporada["descripcion"] if temporada else "Desconocida"
        
    return datas
    
    

@router.post("/Cargar/Uno", response_model=PuntosPorPosicionCarrera, status_code=status.HTTP_201_CREATED)
async def create_puntos(puntos_por_posicion:PuntosPorPosicionCarrera):
     
    dict_puntos = realizar_carga(puntos_por_posicion)
    id = db_client.sistema_de_puntuacion.insert_one(dict_puntos).inserted_id
    new_puntos = punto_schema(db_client.sistema_de_puntuacion.find_one({"_id":id}))
    
    return PuntosPorPosicionCarrera(**new_puntos)

@router.post("/Cargar/Muchos", response_model=list[PuntosPorPosicionCarrera], status_code=status.HTTP_201_CREATED)
async def create_many_puntos(puntos_por_posiciones:list[PuntosPorPosicionCarrera]):
    lista_puntos = []
    for puntos in puntos_por_posiciones:
        dict_puntos = realizar_carga(puntos)
        lista_puntos.append(dict_puntos)
        
    resultado = db_client.sistema_de_puntuacion.insert_many(lista_puntos)
    
    ids = resultado.inserted_ids
    documentos = db_client.sistema_de_puntuacion.find({"_id":{"$in":ids}})
    
    news_puntos = puntos_schema(documentos)
    
    return list(news_puntos)

def realizar_carga(puntos):
    temporada_oid = validate_object_id(puntos.temporada)
    datos = {
        "posicion" : puntos.posicion,
        "puntos"   : puntos.puntos,
        "tipo"     : puntos.tipo,
        "temporada": temporada_oid
        }
    temporada = db_client.temporadas.find_one({"_id":temporada_oid})
    
    if db_client.sistema_de_puntuacion.find_one(datos):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                            detail=f"La posicion {puntos.posicion} de la '{temporada["descripcion"]}' para el tipo de carrera {puntos.tipo} ya estan cargados")
    
    dict_puntos = dict(puntos)
    del dict_puntos["id"]
    dict_puntos["temporada"] = temporada_oid
    return dict_puntos
    
        
@router.delete("/Borrar/Todo/{temporada}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_data_by_type_and_category(temporada:str):
    temporada_oid = validate_object_id(temporada)
    borrado = db_client.sistema_de_puntuacion.delete_many({"temporada":temporada_oid})
    
    if not borrado:
         raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="No se encontro el circuito que se desea eliminar")
    




def search_data(key:str, value):
    try:
        equipo = db_client.puntosxposicion.find_one({key:value})
        return PuntosPorPosicionCarrera(**punto_schema(equipo))
    except:
        return {"ERROR": "Datos no encontrado"}