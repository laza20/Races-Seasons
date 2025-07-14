from pydantic import BaseModel

class Equipos(BaseModel):
    id                  : str | None = None
    nombre_equipo       : str
    pais_equipo         : str
    tipo                : str
    estado              : bool
    
class EquipoCarga(BaseModel):
    nombre_equipo       : str
    pais_equipo         : str
    tipo                : str
    estado              : bool
    
class EquiposPorTemporada(BaseModel):
    id                          : str | None = None
    nombre_equipo               : str
    pais_equipo                 : str | None = None
    equipo_actual               : str | None = None 
    temporada                   : str
    tipo                        : str | None = None
    estado                      : bool
    
class EquiposPorTemporadaCarga(BaseModel):
    nombre_equipo               : str
    temporada                   : str
    estado                      : bool
