from fastapi import APIRouter
from db.models.pilotos import Piloto, PilotoCarga
from db.schemas.pilotos import piloto_schema, pilotos_schema, piloto_carga_schema, pilotos_carga_schema
from peticiones_http import peticiones_http_delete, peticiones_http_get, peticiones_http_post, peticiones_http_put
from Validaciones import validar_piloto


router = APIRouter(prefix="/Pilotos",
                   tags=["Pilotos"], 
                   responses={404:{ "message":"No encontrado"}})
    
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

peticiones_http_get.view_old_data(
    router, 
    "Pilotos", 
    Piloto, 
    pilotos_schema
)

peticiones_http_get.view_data_by_id(
    router, 
    "Pilotos", 
    Piloto, 
    piloto_schema
)

    