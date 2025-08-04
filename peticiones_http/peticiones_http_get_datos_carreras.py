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
from db.models.carreras import Carreras, CarrerasCarga
from db.schemas.carreras import carreras_carga_schema, carrera_carga_schema
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
        
#Sirve para carreras, carreras_por_piloto, carreras_por_equipos
def view_data_season_and_city(router, base_de_datos, schema):
    @router.get("/Ciudad/{temporada}/{ciudad_circuito}")
    async def show_carreras_city(ciudad_circuito: str, temporada:str):
        coleccion = getattr(db_client, base_de_datos)
        temporada_oid = funciones_logicas.validate_object_id(temporada)
        carreras = schema(coleccion.find({"ciudad_circuito":ciudad_circuito, "temporada": temporada_oid}))
        if not carreras:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontraron carreras")
        
        return carreras
    
def  view_data_for_category_and_year(router, base_de_datos, schema):
    @router.get("/Data/Por/{categoria}/{year}")
    async def view_data_for_category_and_year(categoria:str, year:int ):
        coleccion = getattr(db_client, base_de_datos)
        season = db_client.Temporadas.find_one({"categoria":categoria, "year":year})
        if not season:
            errores_simples.error_simple_negativo(f"{categoria}-{year}", base_de_datos)
        temporada_oid = funciones_logicas.validate_object_id(season["_id"])
        documentos = schema(coleccion.find({"temporada":temporada_oid}))
        return documentos
        
        

