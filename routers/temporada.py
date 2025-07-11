from fastapi import APIRouter, Path,  HTTPException, status
from db.models.temporada import Temporada, TemporadaCarga
from db.client import db_client
from db.schemas.temporada import temporada_schema, temporadas_schema
from bson import ObjectId
from bson.errors import InvalidId
from peticiones_http import peticiones_http_delete, peticiones_http_get, peticiones_http_post, peticiones_http_put
from Validaciones import validar_temporada

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
    validar_temporada.validar_carga_temporada
)

peticiones_http_post.cargar_muchos(
    TemporadaCarga,
    router,
    "Temporadas",
    temporadas_schema,
    validar_temporada.validar_carga_temporada    
)

peticiones_http_get.view_old_data(
    router, 
    "Temporadas", 
    Temporada, 
    temporadas_schema
)

peticiones_http_get.view_data_by_id(
    router, 
    "Temporadas", 
    Temporada, 
    temporada_schema
)




