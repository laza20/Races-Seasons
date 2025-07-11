#pyright: reportInvalidTypeForm=false
from funciones import funciones_carga
from fastapi import status, Body
from pydantic import BaseModel
from db.client import db_client
from typing import Type, Any, List

def view_old_data(router, base_de_datos, Clase: Type[BaseModel], schema):
    @router.get("/Ver/Todo", response_model=list[Clase])
    async def show_many_data():
        coleccion = getattr(db_client, base_de_datos)
        return schema(coleccion.find())
