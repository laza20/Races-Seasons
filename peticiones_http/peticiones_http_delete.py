#pyright: reportInvalidTypeForm=false
from fastapi import status
from db.client import db_client
from fastapi import  HTTPException, status

def delete_old_by_type(router, base_de_datos):
    @router.delete("/Borrar/Todo", status_code=status.HTTP_202_ACCEPTED)
    async def delete_old_teams():
        coleccion = getattr(db_client, base_de_datos)
        borrado = coleccion.delete_many({"tipo":base_de_datos})
        if not borrado:
            raise HTTPException(status_code=404, detail="Datos no encontrados")