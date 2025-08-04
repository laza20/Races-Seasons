from fastapi import APIRouter
from db.schemas.puntos_por_equipos import puntos_por_equipo_schema, puntos_por_equipos_schema
from db.models.puntos_por_equipos import PuntosXEquipo
from peticiones_http import peticiones_http_delete, peticiones_http_get, peticiones_http_put, peticiones_http_get_datos_carreras

router = APIRouter(prefix="/Carreras/Por/Equipos",
                   tags=["Carreras por equipos"],
                   responses={404:{"Message":"No encontrado"}}
)
base_de_datos = "Carreras_por_equipos"

peticiones_http_get.view_old_data(
    router, 
    base_de_datos, 
    PuntosXEquipo, 
    puntos_por_equipos_schema    
)

lista_de_datos_str_plural= ["fecha" ]
peticiones_http_delete.delete_many_by_data_str(
    router, 
    base_de_datos, 
    lista_de_datos_str_plural)

peticiones_http_get_datos_carreras.view_data_season_and_city(
    router,
    base_de_datos,
    puntos_por_equipos_schema
)

peticiones_http_get_datos_carreras.view_data_for_category_and_year(
    router,
    base_de_datos, 
    puntos_por_equipos_schema
)