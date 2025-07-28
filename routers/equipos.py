from fastapi import APIRouter
from db.models.equipos import Equipos, EquipoCarga
from db.schemas.equipos import equipo_schema, equipos_schema, equipo_carga_schema, equipos_carga_schema
from peticiones_http import peticiones_http_delete, peticiones_http_get, peticiones_http_post, peticiones_http_put
from validaciones import validar_equipo


router = APIRouter(prefix="/Equipos",
                   tags=["Equipos"], 
                   responses={404:{ "message":"No encontrado"}})

base_de_datos ="Equipos"  
    
peticiones_http_post.cargar_uno(
    EquipoCarga,
    router,
    base_de_datos,
    equipo_schema,
    validar_equipo.validacion_carga_equipo
)

peticiones_http_post.cargar_muchos(
    EquipoCarga,
    router,
    base_de_datos,
    equipos_schema,
    validar_equipo.validacion_carga_equipo    
)

peticiones_http_get.view_old_data(
    router, 
    base_de_datos, 
    Equipos, 
    equipos_schema
)

lista_de_propiedades_str_sing = ["nombre_equipo"]

peticiones_http_get.view_one_document_for_data_str(
    router, 
    "nombre_equipo", 
    equipos_schema, 
    lista_de_propiedades_str_sing
    )

peticiones_http_get.view_data_charge(
    router, 
    equipos_carga_schema, 
    EquipoCarga,
    "" ,#Solo si es una base de datos de temporada,
    "",#campo que modifica
    ""#Campo que busca
    )


peticiones_http_get.view_data_by_id(
    router, 
    base_de_datos, 
    Equipos, 
    equipo_schema
)

peticiones_http_delete.delete_old_by_type(
    router,
    base_de_datos
)

peticiones_http_delete.delete_one_by_id(
    router,
    base_de_datos
)