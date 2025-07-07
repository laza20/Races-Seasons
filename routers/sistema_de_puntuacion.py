from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from db.models.sistema_de_puntuacion import PuntosPorPosicionCarrera , PuntosPorPosicionCarreraCarga
from db.client import db_client
from db.schemas.sistema_de_puntuacion import punto_schema, puntos_schema
from bson import ObjectId
from bson.errors import InvalidId
from funciones import peticiones_http_delete, peticiones_http_get, peticiones_http_post, peticiones_http_put, validaciones

router = APIRouter(prefix="/Sistema/Puntuacion",
                   tags=["Sistema de puntuacion"], 
                   responses={404:{ "message":"No encontrado"}})

def validate_object_id(id: str):
    try:
        return ObjectId(id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="ID inválido")
    
    
peticiones_http_post.cargar_uno(
    PuntosPorPosicionCarreraCarga,
    router,
    "Sistema_de_puntuacion",
    punto_schema,
    validaciones.validar_carga_sistema_de_puntuacion
)

peticiones_http_post.cargar_muchos(
    PuntosPorPosicionCarreraCarga,
    router,
    "Sistema_de_puntuacion",
    puntos_schema,
    validaciones.validar_carga_sistema_de_puntuacion  
)

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