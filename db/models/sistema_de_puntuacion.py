from pydantic import BaseModel


class PuntosPorPosicionCarrera(BaseModel):
    id                       : str | None = None
    posicion                 : int
    puntos                   : int
    temporada                : str
    tipo                     : str
    estado                   : bool
    
class PuntosPorPosicionCarreraCarga(BaseModel):
    posicion                 : int
    puntos                   : int
    temporada                : str
    tipo                     : str
    estado                   : bool