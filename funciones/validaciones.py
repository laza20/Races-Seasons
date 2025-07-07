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

        
def validar_carga_circuito(datos, base_de_datos):
    coleccion = getattr(db_client, base_de_datos)

    # Si es una lista con más de un circuito
    if isinstance(datos, list) and len(datos) >= 2:
        ciudades = set()
        for dato in datos:
            key = (dato.pais_circuito.lower(), dato.ciudad_circuito.lower())
            
            # Verificar duplicados en la misma carga
            if key in ciudades:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Mismo circuito ingresado 2 veces")
            ciudades.add(key)

            # Verificar si ya existe en la base de datos
            if coleccion.find_one({"pais_circuito": dato.pais_circuito, "ciudad_circuito": dato.ciudad_circuito}):
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"El circuito {dato.ciudad_circuito} ya está cargado")

    else:
        # Es un único circuito
        dato = datos if not isinstance(datos, list) else datos[0]

        if coleccion.find_one({"pais_circuito": dato.pais_circuito, "ciudad_circuito": dato.ciudad_circuito}):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"El circuito {dato.ciudad_circuito} ya está cargado")
        

def validacion_carga_equipo(datos, base_de_datos):
    coleccion = getattr(db_client, base_de_datos)
    if isinstance(datos, list) and len(datos) >= 2:
        equipos = set()
        for dato in datos:
            key = (dato.nombre_equipo.lower(), dato.pais_equipo.lower())
            
            if key in equipos:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Mismo Equipo ingresado 2 veces")
            equipos.add(key)
            
            if coleccion.find_one({"nombre_equipo": dato.nombre_equipo, "pais_equipo": dato.pais_equipo}):
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"El Equipo {dato.nombre_equipo} ya está cargado")
    else:
        dato = datos if not isinstance(datos, list) else datos[0]

        if coleccion.find_one({"nombre_equipo": dato.nombre_equipo, "pais_equipo": dato.pais_equipo}):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"El Equipo {dato.nombre_equipo} ya está cargado")
        

def validacion_carga_piloto(datos, base_de_datos):
    coleccion = getattr(db_client, base_de_datos)
    if isinstance(datos, list) and len(datos) >= 2:
        pilotos = set()
        for dato in datos:
            key = (dato.piloto_participante.lower(), dato.edad_piloto)
            
            if key in pilotos:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Mismo piloto ingresado 2 veces")
            pilotos.add(key)
            

            if coleccion.find_one({"piloto_participante": dato.piloto_participante, "edad_piloto": dato.edad_piloto}):
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"El piloto {dato.piloto_participante} ya está cargado")
    else:
        dato = datos if not isinstance(datos, list) else datos[0]

        if coleccion.find_one({"piloto_participante": dato.piloto_participante, "edad_piloto": dato.edad_piloto}):
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"El piloto {dato.piloto_participante} ya está cargado")
        
        
def validar_carga_sistema_de_puntuacion(datos, base_de_datos):
    coleccion = getattr(db_client, base_de_datos)
    if isinstance(datos, list) and len(datos) >= 2:
        puntos = set()
        for dato in datos:
            temporada_oid = funciones_logicas.validate_object_id(dato.temporada)
            key = (dato.posicion.lower(), dato.puntos, dato.tipo.capitalize(), temporada_oid)
            
            if key in puntos:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Sistema de puntos ya ingresados")
            puntos.add(key)
            
            if not db_client.Temporadas.find_one({"_id": temporada_oid}):
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Temporada incorrecta")
            
            if coleccion.find_one({"posicion": dato.posicion, "puntos": dato.puntos, "tipo": dato.tipo, "temporada":dato.temporada}):
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Sistema de puntos ya ingresados en Base de datos")
    else:
    
        dato = datos if not isinstance(datos, list) else datos[0]
        
        temporada_oid = funciones_logicas.validate_object_id(dato.temporada)

        
        if not db_client.Temporadas.find_one({"_id": temporada_oid}):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Temporada incorrecta")

        if coleccion.find_one({"posicion": dato.posicion, "puntos": dato.puntos, "temporada":dato.temporada, "tipo": dato.tipo}):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Sistema de puntos ya ingresados en Base de datos")