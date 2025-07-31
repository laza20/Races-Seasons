from fastapi import APIRouter
from db.models.carreras import Carreras, CarrerasCarga
from db.schemas.carreras import carrera_schema , carreras_schema
from peticiones_http import peticiones_http_delete, peticiones_http_get, peticiones_http_post, peticiones_http_put
from validaciones import validar_carreras_por_temporada



router = APIRouter(prefix="/Carreras",
                   tags=["Carreras"],
                   responses={404:{"Message":"No encontrado"}}
)

base_de_datos ="Carreras" 
    
peticiones_http_post.cargar_uno_carrera(
    Carreras,  
    router,
    base_de_datos,
    "",
    validar_carreras_por_temporada.validar_carga_carrera_por_temporada
) 

peticiones_http_post.cargar_muchos_carrera(
    Carreras,  
    router,
    base_de_datos,
    "",
    validar_carreras_por_temporada.validar_carga_carrera_por_temporada
)

peticiones_http_get.view_old_data(
    router, 
    base_de_datos, 
    Carreras, 
    carreras_schema    
)

peticiones_http_get.view_data_charge(
    router, 
    carreras_schema, 
    CarrerasCarga,
    "" ,#Solo si es una base de datos de temporada,
    "",#campo que modifica
    ""#Campo que busca
    )

peticiones_http_get.view_data_by_id(
    router, 
    base_de_datos, 
    Carreras, 
    carrera_schema
)

peticiones_http_get.view_many_data_by_id(
    router, 
    base_de_datos, 
    Carreras, 
    carreras_schema
)

lista_de_datos_str_plural= ["fecha" ]
peticiones_http_delete.delete_many_by_data_str(
    router, 
    base_de_datos, 
    lista_de_datos_str_plural)

