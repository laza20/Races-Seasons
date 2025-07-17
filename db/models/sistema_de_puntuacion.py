from pydantic import BaseModel


class PuntosPorPosicionCarrera(BaseModel):
    id                       : str | None = None
    posicion                 : int
    puntos                   : int
    temporada                : str
    tipo                     : str | None = None
    tipo_carrera             : str
    estado                   : bool
    
class PuntosPorPosicionCarreraCarga(BaseModel):
    posicion                 : int
    puntos                   : int
    temporada                : str
    tipo                     : str
    tipo_carrera             : str
    estado                   : bool