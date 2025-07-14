from pydantic import BaseModel

class Piloto(BaseModel):
    id                   : str | None = None
    piloto_participante  : str
    edad_piloto          : int
    nacionalidad_piloto  : str
    tipo                 : str | None = None
    estado               : bool
    
class PilotoCarga(BaseModel):
    piloto_participante  : str
    edad_piloto          : int
    nacionalidad_piloto  : str
    estado               : bool

class PilotoTemporada(BaseModel):
    id                   : str | None = None
    piloto_participante  : str 
    edad_piloto          : int | None = None
    nacionalidad_piloto  : str | None = None
    temporada            : str
    tipo                 : str | None  = None
    estado               : bool
    
class PilotoTemporadaCarga(BaseModel):
    piloto_participante  : str 
    temporada            : str
    estado               : bool

    

