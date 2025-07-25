from db.client import db_client
from fastapi import HTTPException, status
from validaciones_generales.lista_de_campos import listas_de_campos

def validacion_simple_str(base_de_datos, dato):
    coleccion = getattr(db_client, base_de_datos)
    
    if base_de_datos not in listas_de_campos:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"No hay definición de campos para la colección {base_de_datos}")
    
    campos = listas_de_campos[base_de_datos]
    
    for campo in campos:
        query = (
            {campo: {"$regex": f"^{dato}$", "$options": "i"}} if isinstance(dato, str)
            else {campo: dato}
        )
        if coleccion.find_one(query):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"El dato '{dato}' ya se encuentra en la base de datos '{base_de_datos}' en el campo '{campo}'"
            )
        
        
def validacion_simple_negativa_str(base_de_datos, dato):
    coleccion = getattr(db_client, base_de_datos)
    
    if base_de_datos not in listas_de_campos:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"No hay definición de campos para la colección {base_de_datos}")
    
    campos = listas_de_campos[base_de_datos]
    
    for campo in campos:
        query = (
            {campo: {"$regex": f"^{dato}$", "$options": "i"}} if isinstance(dato, str)
            else {campo: dato}
        )
        if coleccion.find_one(query):
            return
        
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=f"El dato '{dato}' no se encuentra en la base de datos '{base_de_datos}'"
        )