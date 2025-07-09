from db.client import db_client
from fastapi import HTTPException, status
from funciones import funciones_logicas
        
        
def validar_carga_temporada(datos, base_de_datos):
    coleccion = getattr(db_client, base_de_datos)
    if isinstance(datos, list) and len(datos) >= 2:
        claves = set()
        key = (dato.year , dato.categoria.lower())
        if key in claves:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Misma temporada ingresada 2 veces")
        claves.add(key)
    else:
        # Es un único circuito
        dato = datos if not isinstance(datos, list) else datos[0]

        if coleccion.find_one({"categoria":dato.categoria, "year":dato.year}):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail =f"Temporada {dato.year} de {dato.categoria} ya existente en la Base de datos")
