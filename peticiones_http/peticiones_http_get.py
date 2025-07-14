#pyright: reportInvalidTypeForm=false
from funciones import funciones_carga, funciones_logicas
from fastapi import status, Body
from pydantic import BaseModel
from db.client import db_client
from typing import Type, Any, List
from funciones import funciones_logicas
from fastapi import APIRouter, HTTPException, status
from db.schemas.temporada import temporada_schema




def view_old_data(router, base_de_datos, Clase: Type[BaseModel], schema):
    @router.get("/Ver/Todo", response_model=list[Clase])
    async def show_many_data():
        coleccion = getattr(db_client, base_de_datos)
        return schema(coleccion.find())
    
def view_one_document_for_data_str(router, base_de_datos, schema, lista_de_propiedades):
    @router.get("/Dato/{data}")
    async def show_many_data_for_data(data:str):
        coleccion = getattr(db_client, base_de_datos)
        for propiedad in lista_de_propiedades:
            resultado = coleccion.find_one({propiedad:{"$regex": f"^{data}$", "$options": "i"}})
            if resultado:
                return schema(resultado)
        
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontro ningun documento con ese dato")    


def view_data_by_id(router, base_de_datos, Clase: Type[BaseModel], schema):
    @router.get("/Buscar/Data/Por/{id}", response_model = Clase)
    async def show_circuito_by_id(id:str):
        try:
            coleccion = getattr(db_client, base_de_datos)
            objeto_id = funciones_logicas.validate_object_id(id)
            return schema(coleccion.find_one({"_id":objeto_id}))
        except:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dato sin id o id incorrecto")
        
        
def view_data_for_season_by_category_and_year(router, campo, base_de_datos, schema, base_de_datos_2):
    @router.get("/Buscar/Datos/De/Cargas/{categoria}/{year}")
    async def show_teams_for_load(categoria:str, year:int):
        coleccion = getattr(db_client, base_de_datos)
        lista=[]
        temporada = funciones_logicas.identificar_temporada(year, categoria)
        temporada_id = temporada["_id"]
        temporada_oid = funciones_logicas.validate_object_id(temporada_id)
        temporada_descripcion = funciones_logicas.transformar_de_id_a_descripcion_o_nombre(temporada_oid, "Temporadas", temporada_schema, base_de_datos_2)
        datas = coleccion.find({"temporada":temporada_oid})
        for data in datas:
            obj = schema(data)
            data_id = data["_id"]
            data_oid = funciones_logicas.validate_object_id(data_id)
            valor = funciones_logicas.transformar_de_id_a_descripcion_o_nombre(
                data_oid, base_de_datos, schema, base_de_datos_2
            )
            dict={
                campo : valor,
                "temporada":temporada_descripcion,
                "estado":obj["estado"]
            }
            lista.append(dict)
        
        return lista