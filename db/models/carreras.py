from pydantic import BaseModel

class Carreras(BaseModel):
    id                       : str | None = None
    piloto_participante      : str
    equipo_participante      : str
    posicion                 : int
    vuelta_rapida_piloto     : str | None = None
    vuelta_rapida_equipo     : str | None = None
    ciudad_circuito          : str
    dnf                      : bool
    fecha                    : str
    temporada                : str
    tipo_carrera             : str
    tipo                     : str | None = None 
    estado                   : bool
    
class CarrerasCarga(BaseModel):
    piloto_participante      : str
    equipo_participante      : str
    posicion                 : int
    vuelta_rapida_piloto     : str | None = None
    vuelta_rapida_equipo     : str | None = None
    ciudad_circuito          : str
    dnf                      : bool
    fecha                    : str
    temporada                : str
    tipo_carrera             : str
    tipo                     : str | None = None 
    estado                   : bool