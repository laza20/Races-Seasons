from pydantic import BaseModel

class PodiosPorPilotoTotal(BaseModel):
    nombre_piloto      : str
    nacionalidad_piloto: str
    edad_piloto        : int
    podios_piloto      : int
    primer_lugar       : int
    segundo_lugar      : int
    tercer_lugar       : int

    
class PodiosPorPilotoTemporada(BaseModel):
    nombre_piloto      : str
    nacionalidad_piloto: str
    edad_piloto        : int
    podios_piloto      : int
    primer_lugar       : int
    segundo_lugar      : int
    tercer_lugar       : int
    temporada          : str

    
class PodiosPorEquipo(BaseModel):
    nombre_equipo      : str
    nacionalidad_equipo: str
    podios_equipo      : int
    primer_lugar       : int
    segundo_lugar      : int
    tercer_lugar       : int
    
class PodiosPorEquipoTemporada(BaseModel):
    nombre_equipo      : str
    nacionalidad_equipo: str
    podios_equipo      : int
    primer_lugar       : int
    segundo_lugar      : int
    tercer_lugar       : int
    temporada          : str