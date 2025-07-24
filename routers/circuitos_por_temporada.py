from fastapi import APIRouter
from db.models.circuitos import CircuitosPorTemporada, CircuitosPorTemporadaCarga
from db.schemas.circuitos import circuito_por_temporada_schema, circuitos_por_temporada_schema, circuito_carga_por_temporada_schema, circuitos_por_temporada_carga_schema
from peticiones_http import peticiones_http_delete, peticiones_http_get, peticiones_http_post, peticiones_http_put
from validaciones import validar_circuito_por_temporada

router = APIRouter(prefix="/Circuitos_Temporada",
                   tags=["Circuitos por temporada"], 
                   responses={404:{ "message":"No encontrado"}})

peticiones_http_post.cargar_uno_temporada(
    CircuitosPorTemporadaCarga,
    router,
    "Circuitos_por_temporada",
    circuito_por_temporada_schema,
    validar_circuito_por_temporada.validar_carga_circuito_por_temporada,
    "ciudad_circuito"
)

peticiones_http_post.cargar_muchos_temporada(
    CircuitosPorTemporadaCarga,
    router,
    "Circuitos_por_temporada",
    circuitos_por_temporada_schema,
    validar_circuito_por_temporada.validar_carga_circuito_por_temporada,
    "ciudad_circuito"
)

peticiones_http_get.view_old_data(
    router, 
    "Circuitos_por_temporada", 
    CircuitosPorTemporada, 
    circuitos_por_temporada_schema
)

lista_de_propiedades_str_sing = ["ciudad_circuito"]

peticiones_http_get.view_one_document_for_data_str(
    router, 
    "Circuitos_por_temporada", 
    circuito_por_temporada_schema, 
    lista_de_propiedades_str_sing
    )

peticiones_http_get.view_data_charge(
    router, 
    circuitos_por_temporada_schema, 
    CircuitosPorTemporadaCarga,
    "Circuitos" ,#Solo si es una base de datos de temporada,
    "circuito",#campo que modifica
    "ciudad_circuito"#Campo que busca
    )


peticiones_http_get.view_data_by_id(
    router, 
    "Circuitos_por_temporada", 
    CircuitosPorTemporada, 
    circuito_por_temporada_schema
)

peticiones_http_get.view_data_for_season_by_category_and_year(
    router,
    "ciudad_circuito", 
    "Circuitos_por_temporada", 
    circuito_por_temporada_schema,
    "Circuitos"
    )

peticiones_http_get.view_data_for_season_by_category_and_year_season_id(
    router,
    "ciudad_circuito", 
    "Circuitos_por_temporada", 
    circuito_por_temporada_schema,
    "Circuitos"
    )


peticiones_http_delete.delete_old_by_type(
    router,
    "Circuitos_por_temporada"
)
    
peticiones_http_delete.delete_one_by_id(
    router,
    "Circuitos_por_temporada"
)