#pyright: reportInvalidTypeForm=false
from fastapi import status
from db.client import db_client
from fastapi import  HTTPException, status
from funciones import funciones_logicas

def delete_old_by_type(router, base_de_datos):
    @router.delete("/Borrar/Todo", status_code=status.HTTP_202_ACCEPTED)
    async def delete_old_teams():
        coleccion = getattr(db_client, base_de_datos)
        borrado = coleccion.delete_many({"tipo":base_de_datos})
        if not borrado:
            raise HTTPException(status_code=404, detail="Datos no encontrados")
        
def delete_one_by_id(router, base_de_datos):
    @router.delete("/Borrar/Por/{id}", status_code=status.HTTP_204_NO_CONTENT)
    async def delete_equipo(id:str):
        coleccion = getattr(db_client, base_de_datos)
        oid = funciones_logicas.validate_object_id(id)
        borrado = coleccion.find_one_and_delete({"_id": oid})
        if not borrado:
            raise HTTPException(status_code=404, detail="Equipo no encontrado")
        
def delete_many_by_data_str(router, base_de_datos, lista_datos):
    @router.delete("/Borrar/Por/Data/{data}", status_code=status.HTTP_204_NO_CONTENT)
    async def delete_by_data(data:str):
        encontrado = "False"
        coleccion = getattr(db_client, base_de_datos)
        for dato in lista_datos:
            datos = coleccion.find_one({dato:data})
            coleccion.delete_many({dato:data})
            if datos:
                encontrado = "True"
        
        if encontrado != "True":   
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"No se ah encontrado ningun dato {data}, con la propiedad {dato} en los documentos {base_de_datos}")
        
#si elimina una carrera busca los documentos relacionados con esa carrera en las otras tablas
#y los elimina, temporada, fecha y tipo_carrera
def delete_data_by_races(router, base_de_datos):
    @router.delete("/Borrar/Datos/Carrera/{temporada}/{fecha}/{tipo_carrera}", status_code=status.HTTP_204_NO_CONTENT)
    async def delete_races_many_diferents_documents(temporada:str, fecha:str, tipo_carrera:str):
        coleccion = getattr(db_client, base_de_datos)
        temporada_oid = funciones_logicas.validate_object_id(temporada)
        borrado_carrera = coleccion.delete_many({"temporada":temporada_oid, "fecha":fecha, "tipo_carrera":{"$regex": f"^{tipo_carrera}$", "$options": "i"}})
        borrado_carrera_piloto = db_client.Carreras_por_pilotos.delete_many({"temporada":temporada_oid, "fecha":fecha, "tipo_carrera":{"$regex": f"^{tipo_carrera}$", "$options": "i"}})
        borrado_carrera_equipos = db_client.Carreras_por_equipos.delete_many({"temporada":temporada_oid, "fecha":fecha, "tipo_carrera":{"$regex": f"^{tipo_carrera}$", "$options": "i"}})
        
        if not  borrado_carrera and borrado_carrera_equipos and borrado_carrera_piloto:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Los datos ingresados para eliminar de las 3 tablas no fueron correctos.")
        