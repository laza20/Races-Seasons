from pydantic import BaseModel
from typing import List
from db.models.carreras import Carreras
from db.models.puntos_por_equipos import PuntosXEquipo
from db.models.puntos_por_pilotos import PuntosXPiloto

class DatosTotales(BaseModel):
    carreras: List[Carreras]
    puntos_x_equipo: List[PuntosXEquipo]
    puntos_x_piloto: List[PuntosXPiloto]