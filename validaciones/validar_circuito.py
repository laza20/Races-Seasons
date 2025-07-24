from db.client import db_client
from fastapi import HTTPException, status
from funciones import funciones_logicas
        

        
def validar_carga_circuito(datos, base_de_datos):
    coleccion = getattr(db_client, base_de_datos)

    # Si es una lista con más de un circuito
    if isinstance(datos, list) and len(datos) >= 2:
        ciudades = set()
        for dato in datos:
            key = validar_carga_circuito_2(dato)
            if key in ciudades:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Mismo circuito ingresado 2 veces")
            ciudades.add(key)
    else:
        # Es un único circuito
        dato = datos if not isinstance(datos, list) else datos[0]
        key = validar_carga_circuito_2(dato)

        
        
def validar_carga_circuito_2(dato):
    key = (dato.pais_circuito.lower(), dato.ciudad_circuito.lower())
    
    if db_client.Circuitos.find_one({"pais_circuito": dato.pais_circuito, "ciudad_circuito": dato.ciudad_circuito}):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"El circuito {dato.ciudad_circuito} ya está cargado")
        
    return key