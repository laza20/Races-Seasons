from pydantic import BaseModel

class TablaPosicionCampeonato(BaseModel):
    posicion             : int
    nombre               : str
    puntos               : int
    cantidad_de_carreras : int
    temporada            : str
    categoria            : str
    year                 : int
    

class TablaPosicionesCircuito(BaseModel):
    posicion  : int
    nombre    : str
    puntos    : int
    circuito  : str
    temporada : str
    categoria : str
    year      : int
