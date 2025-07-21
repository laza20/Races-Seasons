from pydantic import BaseModel

class PuntosXPiloto(BaseModel):
    id                       : str | None = None
    piloto_participante      : str
    puntos_piloto            : int
    ciudad_circuito          : str
    dnf                      : bool
    fecha                    : str
    temporada                : str
    tipo_carrera             : str
    tipo                     : str | None = None
    estado                   : bool
    
