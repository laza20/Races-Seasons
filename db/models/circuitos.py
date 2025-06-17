from pydantic import BaseModel

class Circuitos(BaseModel):
    id                       : str | None = None
    pais_circuito            : str
    ciudad_circuito          : str
    distancia_del_circuito   : float
    sistema_medicion         : str
    tipo                     : str | None = None
    estado                   : bool
    
class CircuitosCarga(BaseModel):
    pais_circuito            : str
    ciudad_circuito          : str
    distancia_del_circuito   : float
    sistema_medicion         : str
    tipo                     : str | None = None
    estado                   : bool
    
class CircuitosPorTemporada(BaseModel):
    id                       : str   | None = None
    circuito                 : str
    pais_circuito            : str   | None = None
    ciudad_circuito          : str   | None = None
    distancia_del_circuito   : float | None = None
    temporada                : str
    tipo                     : str   | None = None
    estado                   : bool
    
class CircuitosPorTemporadaCarga(BaseModel):
    circuito                 : str #id del circuito
    temporada                : str
    estado                   : bool
    