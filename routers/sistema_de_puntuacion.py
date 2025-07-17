from fastapi import APIRouter
from db.models.sistema_de_puntuacion import PuntosPorPosicionCarrera , PuntosPorPosicionCarreraCarga
from db.client import db_client
from db.schemas.sistema_de_puntuacion import punto_schema, puntos_schema, punto_temporada_schema, puntos_temporada_schema
from peticiones_http import peticiones_http_delete, peticiones_http_get, peticiones_http_post, peticiones_http_put
from Validaciones import validar_sistema_de_puntuacion

router = APIRouter(prefix="/Sistema_puntuacion",
                   tags=["Sistema de puntuacion"], 
                   responses={404:{ "message":"No encontrado"}})

    
peticiones_http_post.cargar_uno(
    PuntosPorPosicionCarreraCarga,
    router,
    "Sistema_de_puntuacion",
    punto_schema,
    validar_sistema_de_puntuacion.validar_carga_sistema_de_puntuacion
)

peticiones_http_post.cargar_muchos(
    PuntosPorPosicionCarreraCarga,
    router,
    "Sistema_de_puntuacion",
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
    "Sistema_de_puntuacion", 
    PuntosPorPosicionCarrera, 
    puntos_schema
)

peticiones_http_get.view_data_by_id(
    router, 
    "Sistema_de_puntuacion", 
    PuntosPorPosicionCarrera, 
    punto_schema
)

peticiones_http_delete.delete_old_by_type(
    router,
    "Sistema_de_puntuacion"
)

peticiones_http_delete.delete_one_by_id(
    router,
    "Sistema_de_puntuacion"
)