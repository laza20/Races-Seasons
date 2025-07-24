from db.client import db_client
from fastapi import HTTPException, status
from funciones import funciones_logicas

coleccion = getattr(db_client, "Temporadas")

def validar_temporada_mediante_categoria_y_year(categoria, year):
    if coleccion.find_one({"categoria":categoria, "year":year}):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail =f"Temporada {year} de {categoria} ya existente en la Base de datos")
