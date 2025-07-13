from fastapi import APIRouter
from db.models.equipos import Equipos, EquiposPorTemporada
from db.schemas.equipos import equipo_schema, equipos_schema, equipo_historico_schema, equipos_historicos_schema
from peticiones_http import peticiones_http_delete, peticiones_http_get, peticiones_http_post, peticiones_http_put
from Validaciones import validar_equipo_por_temporada




router = APIRouter(prefix="/Equipos_Temporada",
                   tags=["Equipos por temporada"], 
                   responses={404:{ "message":"No encontrado"}})


peticiones_http_post.cargar_uno_temporada(
    EquiposPorTemporada,
    router,
    "Equipos_por_temporada",
    equipo_historico_schema,
    validar_equipo_por_temporada.validar_carga_equipo_por_temporada,
    "nombre_equipo"
)

peticiones_http_post.cargar_muchos_temporada(
    EquiposPorTemporada,
    router,
    "Equipos_por_temporada",
    equipos_historicos_schema,
    validar_equipo_por_temporada.validar_carga_equipo_por_temporada,
    "nombre_equipo"
)

peticiones_http_get.view_old_data(
    router, 
    "Equipos_por_temporada", 
    EquiposPorTemporada, 
    equipos_historicos_schema
)

peticiones_http_get.view_data_by_id(
    router, 
    "Equipos_por_temporada", 
    EquiposPorTemporada, 
    equipo_historico_schema
    )

peticiones_http_get.view_data_for_season_by_category_and_year(
    router,
    "nombre_equipo", 
    "Equipos_por_temporada", 
    equipo_historico_schema,
    "Equipos"
    )

peticiones_http_delete.delete_old_by_type(
    router,
    "Equipos_por_temporada"
)