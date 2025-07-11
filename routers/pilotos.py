from fastapi import APIRouter, Path,  HTTPException, status
from db.models.pilotos import Piloto, PilotoTemporada, PilotoCarga
from db.client import db_client
from db.schemas.pilotos import piloto_schema, pilotos_schema, piloto_carga_schema, pilotos_carga_schema
from bson import ObjectId
from bson.errors import InvalidId
from peticiones_http import peticiones_http_delete, peticiones_http_get, peticiones_http_post, peticiones_http_put
from Validaciones import validar_piloto


router = APIRouter(prefix="/Pilotos",
                   tags=["Pilotos"], 
                   responses={404:{ "message":"No encontrado"}})

def validate_object_id(id: str):
    try:
        return ObjectId(id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="ID inválido")
    
peticiones_http_post.cargar_uno(
    PilotoCarga,
    router,
    "Pilotos",
    piloto_schema,
    validar_piloto.validacion_carga_piloto
)

peticiones_http_post.cargar_muchos(
    PilotoCarga,
    router,
    "Pilotos",
    pilotos_schema,
    validar_piloto.validacion_carga_piloto    
)

@router.get("/", response_model=list[Piloto])
async def show_pilotos():
    return pilotos_schema(db_client.Pilotos.find())

@router.get ("/Ver/{id}")
async def show_piloto_by_id (id:str):
    object_id = validate_object_id(id)
    try:
        return piloto_schema(db_client.pilotos.find_one({"_id": object_id}))
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID sin piloto")

@router.get ("/Nombre/{piloto_participante}")
async def show_pilotos_by_name (piloto_participante:str):
    try:
        piloto = piloto_schema(db_client.pilotos.find_one({"piloto_participante":piloto_participante}))
        if piloto:
            return {"piloto": piloto}
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Piloto no encontrado")
    
@router.get("/Carga", response_model=list[PilotoCarga])
async def show_teams_for_load():
    pilotos = pilotos_carga_schema(db_client.Pilotos.find({"tipo":"Pilotos"}))
    return pilotos
    



@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_piloto(id:str):
        borrado = db_client.pilotos.find_one_and_delete({"_id": ObjectId(id)})
        if not borrado:
             raise HTTPException(status_code=404, detail="Piloto no encontrado")
        


@router.put("/modificar", response_model=Piloto, status_code=status.HTTP_202_ACCEPTED)
async def replace_data_piloto(piloto:Piloto):
    dict_piloto = dict(piloto)
    del dict_piloto["id"]
    try:
        result = db_client.pilotos.find_one_and_replace({"_id": ObjectId(piloto.id)}, dict_piloto)
        if result is None:
            raise HTTPException(status_code=404, detail="Piloto no encontrado")
    except:
        raise HTTPException(status_code=400, detail="No se han realizado modificaciones")

    
    return search_data("_id", ObjectId(piloto.id))



def search_data(key:str, value):
    try:
        piloto = db_client.pilotos.find_one({key:value})
        return Piloto(**piloto_schema(piloto))
    except:
        return {"ERROR": "Datos no encontrado"}
    