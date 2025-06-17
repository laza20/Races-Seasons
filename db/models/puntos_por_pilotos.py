from pydantic import BaseModel

class PuntosXPiloto(BaseModel):
    id                       : str | None = None
    piloto_participante      : str
    puntos_piloto            : int
    ciudad_circuito          : str
    dnf                      : bool
    temporada                : str
    tipo                     : str
    estado                   : bool
    
