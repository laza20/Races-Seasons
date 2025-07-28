from fastapi import APIRouter
from db.models.pilotos import PilotoTemporada, PilotoTemporadaCarga
from db.schemas.pilotos import piloto_schema, pilotos_schema, piloto_por_temporada_schema, pilotos_por_temporada_schema, piloto_por_temporada_carga_schema, pilotos_por_temporada_carga_schema
from peticiones_http import peticiones_http_delete, peticiones_http_get, peticiones_http_post, peticiones_http_put
from validaciones import validar_pilotos_por_temporada

router = APIRouter(prefix="/Pilotos_Temporada",
                   tags=["Pilotos por temporada"], 
                   responses={404:{ "message":"No encontrado"}})

base_de_datos = "Pilotos_por_temporada"

peticiones_http_post.cargar_uno_temporada(
    PilotoTemporada,
    router,
    base_de_datos,
    piloto_por_temporada_schema,
    validar_pilotos_por_temporada.validar_carga_piloto_por_temporada,
    "piloto_participante"
)

peticiones_http_post.cargar_muchos_temporada(
    PilotoTemporada,
    router,
    base_de_datos,
    pilotos_por_temporada_schema,
    validar_pilotos_por_temporada.validar_carga_piloto_por_temporada,
    "piloto_participante"
)

peticiones_http_get.view_old_data(
    router, 
    base_de_datos, 
    PilotoTemporada, 
    pilotos_por_temporada_schema
)

lista_de_propiedades_str_sing = ["piloto_participante"]

peticiones_http_get.view_one_document_for_data_str(
    router, 
    base_de_datos, 
    pilotos_por_temporada_schema, 
    lista_de_propiedades_str_sing
    )

peticiones_http_get.view_data_charge(
    router, 
    pilotos_por_temporada_carga_schema, 
    PilotoTemporadaCarga,
    "Pilotos" ,#Solo si es una base de datos de temporada,
    "piloto_participante",#campo que modifica
    "piloto_participante"#Campo que busca
    )

peticiones_http_get.view_data_by_id(
    router, 
    base_de_datos, 
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

peticiones_http_get.view_data_for_season_by_category_and_year_season_id(
    router,
    "piloto_participante", 
    base_de_datos, 
    piloto_por_temporada_schema,
    "Pilotos"
    )

peticiones_http_delete.delete_old_by_type(
    router,
    base_de_datos
)

peticiones_http_delete.delete_one_by_id(
    router,
    base_de_datos
)