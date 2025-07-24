from db.client import db_client
from fastapi import HTTPException, status
from funciones import funciones_logicas
from validaciones_generales import validaciones_generales
        
        
def validar_carga_temporada(datos, base_de_datos):
    if isinstance(datos, list) and len(datos) >= 2:
        claves = set()
        for dato in datos:
            key  = validar_carga_temporada_2(dato, base_de_datos)
            if key in claves:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Misma temporada ingresada 2 veces")
            claves.add(key)
    else:
        # Es un único circuito
        dato = datos if not isinstance(datos, list) else datos[0]
        key  = validar_carga_temporada_2(dato, base_de_datos)
        
def validar_carga_temporada_2(dato, base_de_datos):
    key = (dato.year , dato.categoria.lower())
    validaciones_generales.validacion_doble(base_de_datos, dato.categoria, dato.year)
    return key