from fastapi import APIRouter, Path,  HTTPException, status
from db.models.temporada import Temporada, TemporadaCarga
from db.client import db_client
from db.schemas.temporada import temporada_schema, temporadas_schema
from bson import ObjectId
from bson.errors import InvalidId
from funciones import peticiones_http_delete, peticiones_http_get, peticiones_http_post, peticiones_http_put, validaciones

router = APIRouter(prefix="/Temporada",
                   tags=["Temporada"], 
                   responses={404:{ "message":"No encontrado"}})

def validate_object_id(id: str):
    try:
        return ObjectId(id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="ID inválido")
    
peticiones_http_post.cargar_uno(
    TemporadaCarga,
    router,
    "Temporadas",
    temporada_schema,
    validaciones.validar_carga_temporada
)

@router.get("/Ver/Datos")
async def show_seasons():
    temporadas = temporadas_schema(db_client.temporadas.find())
    if not temporadas:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="No se han encontrado temporadas")
    
    return temporadas




