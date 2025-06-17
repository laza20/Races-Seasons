from pydantic import BaseModel

class ConformacionDeEquipos(BaseModel):
    id                  : str | None = None
    nombre_equipo       : str
    primer_piloto       : str
    segundo_piloto      : str
    piloto_reserva      : str | None = None
    otro_piloto         : str | None = None
    otro_piloto_dos     : str | None = None
    temporada           : str
    tipo                : str
    estado              : bool
    
class ConformacionDeEquiposCarga(BaseModel):
    nombre_equipo       : str
    primer_piloto       : str
    segundo_piloto      : str
    piloto_reserva      : str | None = None
    otro_piloto         : str | None = None
    otro_piloto_dos     : str | None = None
    temporada           : str
    tipo                : str
    estado              : bool