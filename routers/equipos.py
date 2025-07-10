from fastapi import APIRouter, HTTPException, status
from db.models.equipos import Equipos, EquipoCarga
from db.client import db_client
from db.schemas.equipos import equipo_schema, equipos_schema, equipo_carga_schema, equipos_carga_schema
from bson import ObjectId
from bson.errors import InvalidId
from peticiones_http import peticiones_http_delete, peticiones_http_get, peticiones_http_post, peticiones_http_put
from Validaciones import validar_equipo


router = APIRouter(prefix="/Equipos",
                   tags=["Equipos"], 
                   responses={404:{ "message":"No encontrado"}})

def validate_object_id(id: str):
    try:
        return ObjectId(id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="ID inválido")
    
peticiones_http_post.cargar_uno(
    EquipoCarga,
    router,
    "Equipos",
    equipo_schema,
    validar_equipo.validacion_carga_equipo
)

peticiones_http_post.cargar_muchos(
    EquipoCarga,
    router,
    "Equipos",
    equipos_schema,
    validar_equipo.validacion_carga_equipo    
)

@router.get("/", response_model=list[Equipos])
async def show_equipos():
    return equipos_schema(db_client.Equipos.find())

@router.get("/Buscar/{id}")
async def show_equipo(id:str):
    try:
        object_id = validate_object_id(id)
        return equipo_schema(db_client.equipos.find_one({"_id":object_id}))
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID sin equipo")
    
@router.get("/Nombre/{nombre_equipo}")
async def show_equipo_by_id(nombre_equipo:str):
    equipo = equipo_schema(db_client.equipos.find_one({"nombre_equipo":nombre_equipo}))
    if not equipo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail="No se encontro ningun equipo con ese nombre")
    
    return equipo

@router.get("/Pais/{pais_equipo}")
async def show_equipos_by_pais(pais_equipo:str):
    equipos = equipos_schema(db_client.equipos.find({"pais_equipo":pais_equipo}))
    
    if not equipos:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail="No se encontro ningun equipo de ese pais")
        
    return equipos

    

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_equipo(id:str):
    borrado = db_client.equipos.find_one_and_delete({"_id":ObjectId(id)})
    if not borrado:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    
    
@router.delete("/Borrar/Equipos/{categoria}", status_code=status.HTTP_202_ACCEPTED)
async def delete_equipos(categoria:str):
        borrado = db_client.equipos.delete_many({"categoria": categoria})
        if not borrado:
             raise HTTPException(status_code=404, detail="Categoria no encontrado")
    
@router.put("/", response_model=Equipos,  status_code=status.HTTP_202_ACCEPTED)
async def replace_data_equipo(equipo:Equipos):
    dict_equipo = dict(equipo)
    del dict_equipo["id"]
    dict_equipo["tipo"] = "Equipo"
    try:
        result = db_client.equipos.find_one_and_replace({"_id":ObjectId(equipo.id)}, dict_equipo)
        if result is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Equipo no encontrado")
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "No se han realizado las modificaciones")
    
    return search_data("_id", ObjectId(equipo.id))

def search_data(key:str, value):
    try:
        equipo = db_client.equipos.find_one({key:value})
        return Equipos(**equipo_schema(equipo))
    except:
        return {"ERROR": "Datos no encontrado"}