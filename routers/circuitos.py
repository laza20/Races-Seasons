from fastapi import APIRouter
from db.models.circuitos import Circuitos, CircuitosCarga
from db.client import db_client
from db.schemas.circuitos import circuito_schema, circuitos_schema, circuito_carga_schema, circuitos_carga_schema
from peticiones_http import peticiones_http_delete, peticiones_http_get, peticiones_http_post, peticiones_http_put
from validaciones import validar_circuito

router = APIRouter(prefix="/Circuitos",
                   tags=["Circuitos"], 
                   responses={404:{ "message":"No encontrado"}})


    
peticiones_http_post.cargar_uno(
    CircuitosCarga,
    router,
    "Circuitos",
    circuito_schema,
    validar_circuito.validar_carga_circuito
)

peticiones_http_post.cargar_muchos(
    CircuitosCarga,
    router,
    "Circuitos",
    circuitos_schema,
    validar_circuito.validar_carga_circuito    
)

lista_de_propiedades_str_sing = ["ciudad_circuito"]

peticiones_http_get.view_one_document_for_data_str(
    router, 
    "Circuitos", 
    circuito_schema, 
    lista_de_propiedades_str_sing
    )

peticiones_http_get.view_data_charge(
    router, 
    circuitos_carga_schema, 
    CircuitosCarga,
    "" ,#Solo si es una base de datos de temporada,
    "",#campo que modifica
    ""#Campo que busca
    )

peticiones_http_get.view_old_data(
    router, 
    "Circuitos", 
    Circuitos, 
    circuitos_schema
)

peticiones_http_get.view_data_by_id(
    router, 
    "Circuitos", 
    Circuitos, 
    circuito_schema
)

peticiones_http_delete.delete_old_by_type(
    router,
    "Circuitos"
)

peticiones_http_delete.delete_one_by_id(
    router,
    "Circuitos"
)
        
