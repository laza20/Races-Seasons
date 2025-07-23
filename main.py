from fastapi import FastAPI
from routers import pilotos, equipos, circuitos, sistema_de_puntuacion
from routers import  carreras, conformacion_de_equipos
from routers import tabla_posiciones, datos_carreras
from routers import temporada
from routers import equipos_por_temporada, pilotos_por_temporada, circuitos_por_temporada
from routers import users, carreras_por_piloto, carreras_por_equipo


app = FastAPI()


app.include_router(pilotos.router)
app.include_router(equipos.router)
app.include_router(circuitos.router)
app.include_router(sistema_de_puntuacion.router)
app.include_router(conformacion_de_equipos.router)
app.include_router(carreras.router)
app.include_router(tabla_posiciones.router)
app.include_router(datos_carreras.router)
app.include_router(temporada.router)
app.include_router(equipos_por_temporada.router)
app.include_router(pilotos_por_temporada.router)
app.include_router(circuitos_por_temporada.router)
app.include_router(users.router)
app.include_router(carreras_por_piloto.router)
app.include_router(carreras_por_equipo.router)