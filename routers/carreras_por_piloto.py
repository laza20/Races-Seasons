from fastapi import APIRouter
from db.schemas.puntos_por_piloto import puntos_por_piloto_schema, puntos_por_pilotos_schema
from db.models.puntos_por_pilotos import PuntosXPiloto
from peticiones_http import peticiones_http_delete, peticiones_http_get, peticiones_http_put

router = APIRouter(prefix="/Carreras/Por/Piloto",
                   tags=["Carreras por piloto"],
                   responses={404:{"Message":"No encontrado"}}
)

peticiones_http_get.view_old_data(
    router, 
    "Carreras_por_pilotos", 
    PuntosXPiloto, 
    puntos_por_pilotos_schema    
)