from db.client import db_client
from fastapi import HTTPException, status
from validaciones_generales.lista_de_campos import listas_de_campos

def validacion_doble_general(base_de_datos, dato_uno, dato_dos):
    if base_de_datos not in listas_de_campos:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No hay definición de campos para la colección {base_de_datos}"
        )
    coleccion = getattr(db_client, base_de_datos)
    campos = listas_de_campos[base_de_datos]
    
    if isinstance(dato_uno, str) and isinstance(dato_dos, str):
        validacion_doble_str(coleccion,campos, base_de_datos, dato_uno, dato_dos)
    elif isinstance(dato_uno, str) or isinstance(dato_dos, str):
        validacion_doble_one_str(coleccion,campos, base_de_datos, dato_uno, dato_dos)
    else:
        validacion_doble_no_str(coleccion,campos, base_de_datos, dato_uno, dato_dos)
        
        

def validacion_doble_str(coleccion,campos, base_de_datos, dato_uno, dato_dos):
    for i, campo_uno in enumerate(campos):
        for j, campo_dos in enumerate(campos):
            if i == j:
                continue  # Evita comparar el mismo campo contra sí mismo
            
            query = {
                campo_uno: {"$regex": f"^{dato_uno}$", "$options": "i"},
                campo_dos:{"$regex": f"^{dato_dos}$", "$options": "i"}
            }
            
            if coleccion.find_one(query):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Ya existe un documento en '{base_de_datos}' con {campo_uno} = '{dato_uno}' y {campo_dos} = '{dato_dos}'"
                )
    
def validacion_doble_one_str(coleccion,campos, base_de_datos, dato_uno, dato_dos):
    
    for i, campo_uno in enumerate(campos):
        for j, campo_dos in enumerate(campos):
            if i == j:
                continue  # Evita comparar el mismo campo contra sí mismo
            if isinstance(dato_uno, str):
                query = {
                campo_uno: {"$regex": f"^{dato_uno}$", "$options": "i"},
                campo_dos: dato_dos
                }
            
                if coleccion.find_one(query):
                    raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Ya existe un documento en '{base_de_datos}' con {campo_uno} = '{dato_uno}' y {campo_dos} = '{dato_dos}'"
                    )
            else:
                query = {
                campo_uno: dato_uno,
                campo_dos: {"$regex": f"^{dato_dos}$", "$options": "i"},
                }
                
                if coleccion.find_one(query):
                    raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Ya existe un documento en '{base_de_datos}' con {campo_uno} = '{dato_uno}' y {campo_dos} = '{dato_dos}'"
                    )



def validacion_doble_no_str(coleccion,campos, base_de_datos, dato_uno, dato_dos):
    for i, campo_uno in enumerate(campos):
        for j, campo_dos in enumerate(campos):
            if i == j:
                continue  # Evita comparar el mismo campo contra sí mismo
            
            query = {
                campo_uno : dato_uno,
                campo_dos : dato_dos
            }

            if coleccion.find_one(query):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Ya existe un documento en '{base_de_datos}' con {campo_uno} = '{dato_uno}' y {campo_dos} = '{dato_dos}'"
                )
