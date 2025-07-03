from db.client import db_client
from fastapi import HTTPException, status

def validar_carga_circuito(dato, base_de_datos):
        coleccion = getattr(db_client, base_de_datos)
        filtros={
            "pais_circuito"   :dato.pais_circuito,
            "ciudad_circuito" :dato.ciudad_circuito,   
            }
        
        if coleccion.find_one(filtros):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El circuito que desea ingresar ya esta cargado")
        