from fastapi import APIRouter
from db.models.sistema_de_puntuacion import PuntosPorPosicionCarrera , PuntosPorPosicionCarreraCarga
from db.schemas.sistema_de_puntuacion import punto_schema, puntos_schema, punto_temporada_schema, puntos_temporada_schema
from peticiones_http import peticiones_http_delete, peticiones_http_get, peticiones_http_post, peticiones_http_put
from validaciones import validar_sistema_de_puntuacion

router = APIRouter(prefix="/Sistema_puntuacion",
                   tags=["Sistema de puntuacion"], 
                   responses={404:{ "message":"No encontrado"}})

base_de_datos = "Sistema_de_puntuacion"
    
peticiones_http_post.cargar_uno(
    PuntosPorPosicionCarrera,
    router,
    base_de_datos,
    punto_schema,
    validar_sistema_de_puntuacion.validar_carga_sistema_de_puntuacion
)

peticiones_http_post.cargar_muchos(
    PuntosPorPosicionCarrera,
    router,
    base_de_datos,
    puntos_schema,
    validar_sistema_de_puntuacion.validar_carga_sistema_de_puntuacion  
)

peticiones_http_get.view_data_charge(
    router, 
    puntos_temporada_schema, 
    PuntosPorPosicionCarreraCarga,
    "" ,#Solo si es una base de datos de temporada,
    "",#campo que modifica
    ""#Campo que busca
    )

peticiones_http_get.view_old_data(
    router, 
    base_de_datos, 
    PuntosPorPosicionCarrera, 
    puntos_schema
)

peticiones_http_get.view_data_by_id(
    router, 
    base_de_datos, 
    PuntosPorPosicionCarrera, 
    punto_schema
)

peticiones_http_delete.delete_old_by_type(
    router,
    base_de_datos
)

peticiones_http_delete.delete_one_by_id(
    router,
    base_de_datos
)