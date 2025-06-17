from fastapi import APIRouter, HTTPException, status
from db.models.equipos import Equipos, EquipoCarga
from db.client import db_client
from db.schemas.equipos import equipo_schema, equipos_schema, equipo_carga_schema, equipos_carga_schema
from bson import ObjectId
from bson.errors import InvalidId


router = APIRouter(prefix="/Equipos",
                   tags=["Equipos"], 
                   responses={404:{ "message":"No encontrado"}})

def validate_object_id(id: str):
    try:
        return ObjectId(id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="ID inválido")

@router.get("/", response_model=list[Equipos])
async def show_equipos():
    return equipos_schema(db_client.equipos.find())

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

@router.get("/Cargas", response_model=list[EquipoCarga])
async def show_teams_for_load():
    equipos = equipos_carga_schema(db_client.equipos.find({"tipo":"Equipo"}))
    return equipos
    

    
@router.post("/Cargar/Uno", response_model=Equipos, status_code=status.HTTP_201_CREATED)
async def create_equipo(equipo:Equipos):
    dict_equipo = cargar_equipo(equipo)
    
    id = db_client.equipos.insert_one(dict_equipo).inserted_id
    new_equipo = equipo_schema(db_client.equipos.find_one({"_id":id}))
    
    return Equipos(**new_equipo)

@router.post("/Cargar/Muchos", response_model=list[Equipos], status_code=status.HTTP_201_CREATED)
async def create_many_equipos(equipos:list[Equipos]):
    
    lista_equipos = []
    for equipo in equipos:
        dict_equipo = cargar_equipo(equipo)
        lista_equipos.append(dict_equipo)
        
    resultado = db_client.equipos.insert_many(lista_equipos)
    ids = resultado.inserted_ids
    documentos = db_client.equipos.find({"_id":{"$in": ids }})
    news_equipos = equipos_schema(documentos)
    
    return list(news_equipos)
        
def cargar_equipo(equipo):
        filtros = {
            "nombre_equipo" : {"$regex": f"^{equipo.nombre_equipo}$", "$options": "i"},
            "pais_equipo" : {"$regex": f"^{equipo.pais_equipo}$", "$options": "i"},
            }
        
        if db_client.equipos.find_one(filtros):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El equipo ingresado ya se encuentra en la base de datos")
        
        
        dict_equipo = dict(equipo)
        del dict_equipo["id"]
        dict_equipo["tipo"] = "Equipo"
        return dict_equipo
    

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