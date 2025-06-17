from pydantic import BaseModel

class Carreras(BaseModel):
    id                       : str | None = None
    piloto_participante      : str
    equipo_participante      : str
    posicion                 : int
    ciudad_circuito          : str
    dnf                      : bool
    temporada                : str
    tipo                     : str 
    estado                   : bool
    
class CarrerasCarga(BaseModel):
    piloto_participante      : str
    equipo_participante      : str
    posicion                 : int
    ciudad_circuito          : str
    dnf                      : bool
    temporada                : str
    tipo                     : str 
    estado                   : bool