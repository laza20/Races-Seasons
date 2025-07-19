from pydantic import BaseModel

class PuntosXEquipo(BaseModel):
    id                       : str | None = None
    equipo_participante      : str
    puntos_equipo            : int
    ciudad_circuito          : str
    cant_dnf                 : int
    fecha                    : str
    temporada                : str
    tipo                     : str | None = None
    estado                   : bool
    
    
