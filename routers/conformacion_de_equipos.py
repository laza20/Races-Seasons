from fastapi import APIRouter
from db.models.conformacion_de_equipos import ConformacionDeEquipos, ConformacionDeEquiposCarga
from db.schemas.conformacion_de_equipos import piloto_x_equipo_schema, pilotos_x_equipos_schema, piloto_x_equipo_carga_schema, pilotos_x_equipos_cargas_schema
from peticiones_http import peticiones_http_delete,peticiones_http_get, peticiones_http_post, peticiones_http_put
from validaciones import validar_conformacion_de_equipos

router = APIRouter( prefix="/Conformacion_equipos",
                   tags=["Conformacion de equipos"],
                   responses={404:{ "message":"No encontrado"}})


peticiones_http_post.cargar_uno(
    ConformacionDeEquipos,
    router,
    "Conformacion_de_equipos",
    piloto_x_equipo_schema,
    validar_conformacion_de_equipos.validar_carga_de_conformacion_de_equipos
)
peticiones_http_post.cargar_muchos(
    ConformacionDeEquipos,
    router,
    "Conformacion_de_equipos",
    pilotos_x_equipos_schema,
    validar_conformacion_de_equipos.validar_carga_de_conformacion_de_equipos    
)

lista_de_propiedades_str_sing = ["nombre_equipo"]

peticiones_http_get.view_one_document_for_data_str(
    router, 
    "Conformacion_de_equipos", 
    piloto_x_equipo_schema, 
    lista_de_propiedades_str_sing
    )

peticiones_http_get.view_data_charge(
    router, 
    pilotos_x_equipos_cargas_schema, 
    ConformacionDeEquiposCarga,
    "" ,#Solo si es una base de datos de temporada,
    "",#campo que modifica
    ""#Campo que busca
    )

peticiones_http_get.view_old_data(
    router, 
    "Conformacion_de_equipos", 
    ConformacionDeEquipos, 
    pilotos_x_equipos_schema
)

peticiones_http_get.view_data_by_id(
    router, 
    "Conformacion_de_equipos", 
    ConformacionDeEquipos, 
    piloto_x_equipo_schema
)

peticiones_http_delete.delete_old_by_type(
    router,
    "Conformacion_de_equipos"
)

peticiones_http_delete.delete_one_by_id(
    router,
    "Conformacion_de_equipos"
)