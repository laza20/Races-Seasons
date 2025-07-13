from fastapi import APIRouter
from db.models.equipos import Equipos, EquipoCarga
from db.schemas.equipos import equipo_schema, equipos_schema, equipo_carga_schema, equipos_carga_schema
from peticiones_http import peticiones_http_delete, peticiones_http_get, peticiones_http_post, peticiones_http_put
from Validaciones import validar_equipo


router = APIRouter(prefix="/Equipos",
                   tags=["Equipos"], 
                   responses={404:{ "message":"No encontrado"}})

    
peticiones_http_post.cargar_uno(
    EquipoCarga,
    router,
    "Equipos",
    equipo_schema,
    validar_equipo.validacion_carga_equipo
)

peticiones_http_post.cargar_muchos(
    EquipoCarga,
    router,
    "Equipos",
    equipos_schema,
    validar_equipo.validacion_carga_equipo    
)

peticiones_http_get.view_old_data(
    router, 
    "Equipos", 
    Equipos, 
    equipos_schema
)

peticiones_http_get.view_data_by_id(
    router, 
    "Equipos", 
    Equipos, 
    equipo_schema
)
