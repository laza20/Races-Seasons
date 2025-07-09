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
            key = (dato.posicion, dato.puntos, dato.tipo.capitalize(), dato.temporada)
            
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
        
        
def validar_carga_circuito_por_temporada(datos, base_de_datos):
    coleccion = getattr(db_client, base_de_datos)
    if isinstance(datos, list) and len(datos) >= 2:
        circuitos = set()
        for dato in datos:
            temporada_oid = funciones_logicas.validate_object_id(dato.temporada)
            circuito_oid = funciones_logicas.validate_object_id_or_false(dato.circuito)
            circuito = db_client.Circuitos.find_one({"ciudad_circuito":dato.circuito})
            if not circuito and not circuito_oid:
                raise HTTPException(status_code=400, detail="Circuito no válido")
        
            if circuito:
                dict_circuito = dict(circuito)
                circuito_oid = funciones_logicas.validate_object_id(dict_circuito["_id"])
                
            key = (temporada_oid, circuito_oid)
            
            if key in circuitos:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Circuito duplicado en la entrega")
            circuitos.add(key)
            
        if not db_client.Temporadas.find_one({"_id": temporada_oid}):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Temporada incorrecta")
        
        season = db_client.Temporadas.find_one({"_id": temporada_oid})
        
        limitacion_cantidad_por_temporada(season, temporada_oid, datos, coleccion)
            
        if not db_client.Circuitos.find_one({"_id":circuito_oid}):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Circuito incorrecto (no encontrado en la base de datos)")
            
        if coleccion.find_one({"temporada": temporada_oid, "circuito":circuito_oid}):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Circuito ya ingresado en la temporada")
            
    else:
        dato = datos if not isinstance(datos, list) else datos[0]
        try:
            temporada_oid = funciones_logicas.validate_object_id(dato.temporada)
        except:
            raise HTTPException(status_code=400, detail="ID de la temporada o circuito no válido")
        
        season = db_client.Temporadas.find_one({"_id": temporada_oid})
        
        limitacion_cantidad_por_temporada(season, temporada_oid, dato, coleccion)
        
        circuito_oid = funciones_logicas.validate_object_id_or_false(dato.circuito)
        circuito = db_client.Circuitos.find_one({"ciudad_circuito":dato.circuito})
        if not circuito and not circuito_oid:
            raise HTTPException(status_code=400, detail="Circuito no válido")
        
        if circuito:
            dict_circuito = dict(circuito)
            circuito_oid = funciones_logicas.validate_object_id(dict_circuito["_id"])
            
        if not db_client.Temporadas.find_one({"_id": temporada_oid}):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Temporada incorrecta")
            
        if not db_client.Circuitos.find_one({"_id":circuito_oid}):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Circuito incorrecto (no encontrado en la base de datos)")
            
        if coleccion.find_one({"temporada": temporada_oid, "circuito":circuito_oid}):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Circuito ya ingresado en la temporada")
        
        
        
def limitacion_cantidad_por_temporada(season, temporada_oid, datos, coleccion):
        cantidad_actual = coleccion.count_documents({"temporada": temporada_oid})
        
        cantidad_maxima = season.get("cantidad_de_grandes_premios")
        if not isinstance(cantidad_maxima, int):
            raise HTTPException(status_code=500, detail="El campo 'cantidad_de_grandes_premios' no está bien definido en la temporada")
        
        cantidad_nueva = len(datos) if isinstance(datos, list) else 1
        
        if cantidad_actual + cantidad_nueva > cantidad_maxima:
            raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"No se pueden agregar {cantidad_nueva} circuitos: la temporada ya tiene {cantidad_actual}/{cantidad_maxima}"
            )