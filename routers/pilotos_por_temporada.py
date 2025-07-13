from fastapi import APIRouter
from db.models.pilotos import PilotoTemporada
from db.schemas.pilotos import piloto_schema, pilotos_schema, piloto_por_temporada_schema, pilotos_por_temporada_schema
from peticiones_http import peticiones_http_delete, peticiones_http_get, peticiones_http_post, peticiones_http_put
from Validaciones import validar_pilotos_por_temporada

router = APIRouter(prefix="/Pilotos_Temporada",
                   tags=["Pilotos por temporada"], 
                   responses={404:{ "message":"No encontrado"}})


peticiones_http_post.cargar_uno_temporada(
    PilotoTemporada,
    router,
    "Pilotos_por_temporada",
    piloto_por_temporada_schema,
    validar_pilotos_por_temporada.validar_carga_piloto_por_temporada,
    "piloto_participante"
)

peticiones_http_post.cargar_muchos_temporada(
    PilotoTemporada,
    router,
    "Pilotos_por_temporada",
    pilotos_por_temporada_schema,
    validar_pilotos_por_temporada.validar_carga_piloto_por_temporada,
    "piloto_participante"
)

peticiones_http_get.view_old_data(
    router, 
    "Pilotos_por_temporada", 
    PilotoTemporada, 
    pilotos_por_temporada_schema
)

peticiones_http_get.view_data_by_id(
    router, 
    "Pilotos_por_temporada", 
    PilotoTemporada, 
    piloto_por_temporada_schema
)

peticiones_http_get.view_data_for_season_by_category_and_year(
    router,
    "piloto_participante", 
    "Pilotos_por_temporada", 
    piloto_por_temporada_schema,
    "Pilotos"
    )

peticiones_http_delete.delete_old_by_type(
    router,
    "Pilotos_por_temporada"
)