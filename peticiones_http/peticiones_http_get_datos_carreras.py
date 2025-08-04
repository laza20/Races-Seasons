#pyright: reportInvalidTypeForm=false
from funciones import funciones_logicas
from fastapi import status
from pydantic import BaseModel
from db.client import db_client
from typing import Type, List
from funciones import funciones_logicas
from fastapi import  HTTPException, status
from errores import errores_simples
from db.models.carrera_todos_los_datos import DatosTotales
from db.schemas.carreras_todos_los_datos import carrera_todos_los_datos_schema_todas_las_carrera, carrera_todos_los_datos_schema_una_carrera
from funciones import funciones_busqueda


def view_old_data_of_season(router):
    @router.get("/Totales/{temporada}",  response_model=DatosTotales)
    async def obtener_datos_totales(temporada:str):
        temporada_oid = funciones_logicas.validate_object_id(temporada)
        todas_las_carreras_de_una_temporada = funciones_busqueda.encontrar_muchos_documentos(temporada_oid, "Carreras")
        todas_las_carreras_de_un_piloto_temporada = funciones_busqueda.encontrar_muchos_documentos(temporada_oid, "Carreras_por_pilotos")
        todas_las_carreras_de_un_equipo_temporada = funciones_busqueda.encontrar_muchos_documentos(temporada_oid, "Carreras_por_equipos")

        
        lista_carrera, lista_puntos_equipo, lista_puntos_piloto = [], [], []
        
        for carrera, piloto, equipo in zip(todas_las_carreras_de_una_temporada, todas_las_carreras_de_un_piloto_temporada,todas_las_carreras_de_un_equipo_temporada):
            datos_carrera, datos_equipo, datos_piloto = carrera_todos_los_datos_schema_una_carrera(carrera, piloto, equipo)
            lista_carrera.append(datos_carrera)
            lista_puntos_equipo.append(datos_equipo)
            lista_puntos_piloto.append(datos_piloto)
            
        return  DatosTotales(
            carreras=lista_carrera,
            puntos_x_equipo=lista_puntos_equipo,
            puntos_x_piloto=lista_puntos_piloto
    )
        

