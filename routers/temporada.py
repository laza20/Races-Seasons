from fastapi import APIRouter, Path,  HTTPException, status
from db.models.temporada import Temporada
from db.client import db_client
from db.schemas.temporada import temporada_schema, temporadas_schema
from bson import ObjectId
from bson.errors import InvalidId

router = APIRouter(prefix="/Temporada",
                   tags=["Temporada"], 
                   responses={404:{ "message":"No encontrado"}})

def validate_object_id(id: str):
    try:
        return ObjectId(id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="ID inválido")
    
@router.post("/Cargar/Uno", response_model= Temporada, status_code=status.HTTP_201_CREATED)
async def create_season (temporada:Temporada):
    dict_temporada = realizar_carga(temporada)
    id = db_client.temporadas.insert_one(dict_temporada).inserted_id
    new_temporada = temporada_schema(db_client.temporadas.find_one({"_id":id}))
    
    return Temporada(**new_temporada)

@router.get("/Ver/Datos")
async def show_seasons():
    temporadas = temporadas_schema(db_client.temporadas.find())
    if not temporadas:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="No se han encontrado temporadas")
    
    return temporadas

@router.post("/Cargar/Muchos", response_model=list[Temporada], status_code=status.HTTP_201_CREATED)
async def create_many_seasons(temporadas:list[Temporada]):
    lista_temporadas = []
    vistas_unicas = set()
    for temporada in temporadas:
        clave = (temporada.categoria, temporada.year)
        if clave in vistas_unicas:
            raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Misma temporada ingresada 2 veces"
            )
        vistas_unicas.add(clave)
        dict_temporada = realizar_carga(temporada)
        lista_temporadas.append(dict_temporada)
        
    resultado = db_client.temporadas.insert_many(lista_temporadas)
    ids = resultado.inserted_ids
    documentos = db_client.temporadas.find({"_id":{"$in": ids}})
    news_temporadas = temporadas_schema(documentos)
    
    return list(news_temporadas)


def realizar_carga(temporada):
    filtros = {
            "year": temporada.year,
            "categoria": temporada.categoria
            }
        
    if db_client.temporadas.find_one(filtros):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail =f"Temporada {temporada.year} de {temporada.categoria} ya existente en la Base de datos")
        
    dict_temporada = dict(temporada)
    del dict_temporada["id"]
    dict_temporada["tipo"] = "temporada"
    return dict_temporada