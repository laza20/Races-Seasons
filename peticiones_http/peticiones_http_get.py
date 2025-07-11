#pyright: reportInvalidTypeForm=false
from funciones import funciones_carga
from fastapi import status, Body
from pydantic import BaseModel
from db.client import db_client
from typing import Type, Any, List
from funciones import funciones_logicas
from fastapi import APIRouter, HTTPException, status

def view_old_data(router, base_de_datos, Clase: Type[BaseModel], schema):
    @router.get("/Ver/Todo", response_model=list[Clase])
    async def show_many_data():
        coleccion = getattr(db_client, base_de_datos)
        return schema(coleccion.find())


def view_data_by_id(router, base_de_datos, Clase: Type[BaseModel], schema):
    @router.get("/Buscar/Data/Por/{id}", response_model = Clase)
    async def show_circuito_by_id(id:str):
        try:
            coleccion = getattr(db_client, base_de_datos)
            objeto_id = funciones_logicas.validate_object_id(id)
            return schema(coleccion.find_one({"_id":objeto_id}))
        except:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dato sin id o id incorrecto")