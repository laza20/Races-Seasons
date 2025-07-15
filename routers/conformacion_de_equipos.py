from fastapi import APIRouter, HTTPException, status
import re
from db.client import db_client
from db.models.conformacion_de_equipos import ConformacionDeEquipos, ConformacionDeEquiposCarga
from db.schemas.conformacion_de_equipos import piloto_x_equipo_schema, pilotos_x_equipos_schema
from bson import ObjectId
from bson.errors import InvalidId
from peticiones_http import peticiones_http_delete,peticiones_http_get, peticiones_http_post, peticiones_http_put
from Validaciones import validar_conformacion_de_equipos

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


peticiones_http_get.view_old_data(
    router, 
    "Conformacion_de_equipos", 
    ConformacionDeEquipos, 
    pilotos_x_equipos_schema
)