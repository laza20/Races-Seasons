from fastapi import APIRouter
from db.models.temporada import Temporada, TemporadaCarga
from db.schemas.temporada import temporada_schema, temporadas_schema
from peticiones_http import peticiones_http_delete, peticiones_http_get, peticiones_http_post, peticiones_http_put
from validaciones import validar_temporada

router = APIRouter(prefix="/Temporada",
                   tags=["Temporada"], 
                   responses={404:{ "message":"No encontrado"}})
    
base_de_datos = "Temporadas"    
    
peticiones_http_post.cargar_uno(
    TemporadaCarga,
    router,
    base_de_datos,
    temporada_schema,
    validar_temporada.validar_carga_temporada
)

peticiones_http_post.cargar_muchos(
    TemporadaCarga,
    router,
    base_de_datos,
    temporadas_schema,
    validar_temporada.validar_carga_temporada    
)

peticiones_http_get.view_old_data(
    router, 
    base_de_datos, 
    Temporada, 
    temporadas_schema
)

lista_de_propiedades_str_sing = ["descripcion", "observaciones"]

peticiones_http_get.view_one_document_for_data_str(
    router, 
    base_de_datos, 
    temporada_schema, 
    lista_de_propiedades_str_sing
    )

peticiones_http_get.view_data_by_id(
    router, 
    base_de_datos, 
    Temporada, 
    temporada_schema
)

peticiones_http_delete.delete_old_by_type(
    router,
    base_de_datos
)

peticiones_http_delete.delete_one_by_id(
    router,
    base_de_datos
)
