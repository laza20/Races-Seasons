from pydantic import BaseModel

class Temporada(BaseModel):
    id                          : str | None = None
    descripcion                 : str
    cantidad_de_grandes_premios : int
    cantidad_de_equipos         : int
    observaciones               : str #campeones, curiosidades
    tipo                        : str | None = None
    year                        : int
    categoria                   : str
    estado                      : bool
    
class TemporadaCarga(BaseModel):
    descripcion                 : str
    cantidad_de_grandes_premios : int
    cantidad_de_equipos         : int
    observaciones               : str #campeones, curiosidades
    tipo                        : str | None = None
    year                        : int
    categoria                   : str
    estado                      : bool
