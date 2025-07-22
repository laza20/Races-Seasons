# pyright: reportInvalidTypeForm=false
from funciones import funciones_carga, funcion_carga_carrera
from fastapi import status, Body
from pydantic import BaseModel
from typing import Type, Any, List
from db.models.carrera_todos_los_datos import DatosTotales

def cargar_uno(Clase: Type[BaseModel], router, base_de_datos, schema, validacion):
    @router.post("/Cargar/Uno", response_model=Clase, status_code=status.HTTP_201_CREATED)
    async def create_one(clase: Clase = Body(...)):
        new_document = funciones_carga.cargar_uno(clase, base_de_datos, schema, validacion)
    
        return new_document
    
def cargar_uno_temporada(Clase: Type[BaseModel], router, base_de_datos, schema, validacion, campo):
    @router.post("/Cargar/Uno/Temporada", response_model=Clase, status_code=status.HTTP_201_CREATED)
    async def create_one_season(clase: Clase = Body(...)):
        new_document = funciones_carga.cargar_uno_temporada(clase, base_de_datos, schema, validacion, campo)
    
        return new_document
    
def cargar_uno_carrera(Clase: Type[BaseModel], router, base_de_datos, schema, validacion):
    @router.post("/Cargar/Uno", response_model=DatosTotales, status_code=status.HTTP_201_CREATED)
    async def create_one(clase: Clase = Body(...)):
        new_document = await funcion_carga_carrera.cargar_carrera(
            clase,
            base_de_datos,
            schema,
            validacion
        )
        return new_document
    
def cargar_muchos(Clase: Type[BaseModel], router, base_de_datos, schema, validacion):
    @router.post("/Cargar/Muchos", response_model=List[Clase], status_code=status.HTTP_201_CREATED)
    async def create_many(clase: List[Clase] = Body(...)):
        documentos = funciones_carga.cargar_muchos(clase, base_de_datos, schema, validacion)
        return documentos
    
def cargar_muchos_temporada(Clase: Type[BaseModel], router, base_de_datos, schema, validacion, campo):
    @router.post("/Cargar/Muchos/Temporada", response_model=List[Clase], status_code=status.HTTP_201_CREATED)
    async def create_many_season(clase: List[Clase] = Body(...)):
        documentos = funciones_carga.cargar_muchos_temporada(clase, base_de_datos, schema, validacion, campo)
        return documentos
    
    
def cargar_muchos_carrera(Clase: Type[BaseModel], router, base_de_datos, schema, validacion):
    @router.post("/Cargar/Muchos", response_model=DatosTotales, status_code=status.HTTP_201_CREATED)
    async def create_many_races(datos: list[Clase] = Body(...)):
        new_documents = await funcion_carga_carrera.cargar_muchas_carreras(
            datos,
            base_de_datos,
            schema,
            validacion
        )
        return new_documents