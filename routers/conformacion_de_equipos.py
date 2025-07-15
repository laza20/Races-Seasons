from fastapi import APIRouter, HTTPException, status
import re
from db.client import db_client
from db.models.conformacion_de_equipos import ConformacionDeEquipos, ConformacionDeEquiposCarga
from db.schemas.conformacion_de_equipos import piloto_x_equipo_schema, pilotos_x_equipos_schema
from bson import ObjectId
from bson.errors import InvalidId

router = APIRouter( prefix="/Conformacion_equipos",
                   tags=["Conformacion de equipos"],
                   responses={404:{ "message":"No encontrado"}})


