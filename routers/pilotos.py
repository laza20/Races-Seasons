from fastapi import APIRouter
from db.models.pilotos import Piloto, PilotoCarga
from db.schemas.pilotos import piloto_schema, pilotos_schema, piloto_carga_schema, pilotos_carga_schema
from peticiones_http import peticiones_http_delete, peticiones_http_get, peticiones_http_post, peticiones_http_put
from validaciones import validar_piloto


router = APIRouter(prefix="/Pilotos",
                   tags=["Pilotos"], 
                   responses={404:{ "message":"No encontrado"}})
    
base_de_datos = "Pilotos"
    
peticiones_http_post.cargar_uno(
    PilotoCarga,
    router,
    base_de_datos,
    piloto_schema,
    validar_piloto.validacion_carga_piloto
)

peticiones_http_post.cargar_muchos(
    PilotoCarga,
    router,
    base_de_datos,
    pilotos_schema,
    validar_piloto.validacion_carga_piloto    
)

peticiones_http_get.view_old_data(
    router, 
    base_de_datos, 
    Piloto, 
    pilotos_schema
)

lista_de_propiedades_str_sing = ["piloto_participante"]

peticiones_http_get.view_one_document_for_data_str(
    router, 
    base_de_datos, 
    piloto_schema, 
    lista_de_propiedades_str_sing
    )

peticiones_http_get.view_data_charge(
    router, 
    pilotos_carga_schema, 
    PilotoCarga,
    "" ,#Solo si es una base de datos de temporada,
    "",#campo que modifica
    ""#Campo que busca
    )

peticiones_http_get.view_data_by_id(
    router, 
    base_de_datos, 
    Piloto, 
    piloto_schema
)


peticiones_http_delete.delete_old_by_type(
    router,
    base_de_datos
)

peticiones_http_delete.delete_one_by_id(
    router,
    base_de_datos
)
    