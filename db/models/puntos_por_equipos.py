from pydantic import BaseModel

class PuntosXEquipo(BaseModel):
    id                       : str | None = None
    equipo_participante      : str
    puntos_equipo            : int
    ciudad_circuito          : str
    temporada                : str
    tipo                     : str
    estado                   : bool
    
    
