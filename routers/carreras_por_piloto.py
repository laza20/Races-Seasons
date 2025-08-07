from fastapi import APIRouter
from db.schemas.puntos_por_piloto import puntos_por_piloto_schema, puntos_por_pilotos_schema
from db.models.puntos_por_pilotos import PuntosXPiloto
from peticiones_http import peticiones_http_delete, peticiones_http_get, peticiones_http_put, peticiones_http_get_datos_carreras, peticiones_http_get_tabla_posiciones

router = APIRouter(prefix="/Carreras/Por/Piloto",
                   tags=["Carreras por piloto"],
                   responses={404:{"Message":"No encontrado"}}
)

base_de_datos = "Carreras_por_pilotos"

peticiones_http_get.view_old_data(
    router, 
    base_de_datos, 
    PuntosXPiloto, 
    puntos_por_pilotos_schema    
)

lista_de_datos_str_plural= ["fecha" ]
peticiones_http_delete.delete_many_by_data_str(
    router, 
    base_de_datos, 
    lista_de_datos_str_plural)

peticiones_http_get_datos_carreras.view_data_season_and_city(
    router,
    base_de_datos,
    puntos_por_pilotos_schema
)

peticiones_http_get_datos_carreras.view_data_for_category_and_year(
    router,
    base_de_datos, 
    puntos_por_pilotos_schema
)

peticiones_http_get_datos_carreras.view_data_for_season_city_and_type_race(
    router, 
    base_de_datos, 
    puntos_por_pilotos_schema, 
    "puntos_piloto")

peticiones_http_get_datos_carreras.view_podiums_season_by_id_season(
    router, 
    base_de_datos, 
    puntos_por_pilotos_schema
)

peticiones_http_get_datos_carreras.view_podiums_season_by_category_and_year(
    router, 
    base_de_datos, 
    puntos_por_pilotos_schema
)

peticiones_http_get_datos_carreras.view_olds_podiums_for_driver_or_teams_by_category(
    router, 
    base_de_datos, 
    puntos_por_pilotos_schema
    )

peticiones_http_get_tabla_posiciones.view_positions_teams_for_year_and_category(
    router, 
    base_de_datos, 
    puntos_por_pilotos_schema
)