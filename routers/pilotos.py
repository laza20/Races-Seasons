from fastapi import APIRouter, Path,  HTTPException, status
from db.models.pilotos import Piloto, PilotoTemporada, PilotoCarga
from db.client import db_client
from db.schemas.pilotos import piloto_schema, pilotos_schema, piloto_carga_schema, pilotos_carga_schema
from bson import ObjectId
from bson.errors import InvalidId

router = APIRouter(prefix="/Pilotos",
                   tags=["Pilotos"], 
                   responses={404:{ "message":"No encontrado"}})

def validate_object_id(id: str):
    try:
        return ObjectId(id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="ID inválido")

@router.get("/", response_model=list[Piloto])
async def show_pilotos():
    return pilotos_schema(db_client.pilotos.find())

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
    pilotos = pilotos_carga_schema(db_client.pilotos.find({"tipo":"Piloto"}))
    return pilotos
    
    
        

@router.post("/Cargar/Uno", response_model= Piloto, status_code=status.HTTP_201_CREATED)
async def create_piloto (piloto:Piloto):
    dict_piloto = cargar_piloto(piloto)

    id = db_client.pilotos.insert_one(dict_piloto).inserted_id
    new_piloto = piloto_schema(db_client.pilotos.find_one({"_id":id}))
    
    return Piloto(**new_piloto)


@router.post("/Cargar/Muchos", response_model=list[Piloto], status_code=status.HTTP_201_CREATED)
async def create_many_pilotos(pilotos:list[Piloto]):
    lista_pilotos = []
    for piloto in pilotos:
        if any(c["piloto_participante"] == piloto.piloto_participante for c in pilotos):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Mismo piloto ingresado 2 veces")
        dict_piloto = cargar_piloto(piloto)
        lista_pilotos.append(dict_piloto)
        
    resultado = db_client.pilotos.insert_many(lista_pilotos)
    
    ids = resultado.inserted_ids
    documentos = db_client.pilotos.find({"_id":{"$in": ids}})
    
    news_pilotos = pilotos_schema(documentos)
    
    return list(news_pilotos)

def cargar_piloto(piloto):
        filtros = {
            "piloto_participante": {"$regex": f"^{piloto.piloto_participante}$", "$options": "i"},
            "edad_piloto": piloto.edad_piloto,
            }
        
        if db_client.pilotos.find_one(filtros):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail = "Piloto ya existente en la Base de datos")
        
        dict_piloto = dict(piloto)
        del dict_piloto["id"]
        dict_piloto["tipo"] = "Piloto"
        return dict_piloto

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
    