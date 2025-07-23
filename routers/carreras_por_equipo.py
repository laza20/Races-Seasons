from fastapi import APIRouter
from db.schemas.puntos_por_equipos import puntos_por_equipo_schema, puntos_por_equipos_schema
from db.models.puntos_por_equipos import PuntosXEquipo
from peticiones_http import peticiones_http_delete, peticiones_http_get, peticiones_http_put

router = APIRouter(prefix="/Carreras/Por/Equipos",
                   tags=["Carreras por equipos"],
                   responses={404:{"Message":"No encontrado"}}
)

peticiones_http_get.view_old_data(
    router, 
    "Carreras_por_equipos", 
    PuntosXEquipo, 
    puntos_por_equipos_schema    
)