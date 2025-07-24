from db.client import db_client
from fastapi import HTTPException, status
from funciones import funciones_logicas


#VALIDAR QUE EL PRIMERO Y EL SEGUNDO PILOTO SEAN DIFERENTES
def validar_carga_de_conformacion_de_equipos(datos, base_de_datos):
    coleccion = getattr(db_client, base_de_datos)
    
        # Si es una lista con más de un circuito
    if isinstance(datos, list) and len(datos) >= 2:
        equipos = set()
        for dato in datos:
            key = validar_carga_de_conformacion_de_equipos_2(dato,coleccion, datos)
            # Verificar duplicados en la misma carga
            if key in equipos:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Conformacion de equipo duplicada en la entrega"
                )
            equipos.add(key)

    else:
        # Es un único circuito
        dato = datos if not isinstance(datos, list) else datos[0]
        validar_carga_de_conformacion_de_equipos_2(dato, coleccion,  datos)
                


#Funcion para evitar la duplicidad de la carga de documentos de circuitos por temporada
def validar_carga_de_conformacion_de_equipos_2(dato, coleccion,  datos):
        temporada_oid = funciones_logicas.validate_object_id(dato.temporada)
        conformacion_oid = funciones_logicas.validate_object_id_or_false(dato.id)
        temporada = funciones_logicas.identificar_temporada_por_id(temporada_oid)
        
        key = (temporada_oid, conformacion_oid)
        
        buscar_pilotos = {}
        if dato.primer_piloto and dato.segundo_piloto: 
            buscar_pilotos["primer_piloto"] = dato.primer_piloto.strip()
            buscar_pilotos["segundo_piloto"] = dato.segundo_piloto.strip()
        else:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                    detail="El primer y segundo piloto deben estar cargados")
        if dato.piloto_reserva:
            buscar_pilotos["piloto_reserva"] = dato.piloto_reserva.strip()
        if dato.otro_piloto:
            buscar_pilotos["otro_piloto"] = dato.otro_piloto.strip()
        if dato.otro_piloto_dos:
            buscar_pilotos["otro_piloto_dos"] = dato.otro_piloto_dos.strip()
        
        for clave, nombre in buscar_pilotos.items():
            if not nombre:
                nombre = "Null"
                continue
        
            piloto = db_client.Pilotos.find_one({"piloto_participante": {"$regex": f"^{nombre}$", "$options": "i"}})
            
        
            if not piloto:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"El piloto '{nombre}' en el campo '{clave}' no existe en la BD de pilotos" 
                )
            piloto_oid = piloto["_id"]
            piloto_en_la_temporada = db_client.Pilotos_por_temporada.find_one({
                "piloto_participante": piloto_oid,
                "temporada": temporada_oid
                })
            if not piloto_en_la_temporada:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"El piloto '{nombre}' en el campo '{clave}' no esta cargado en la temporada '{temporada['descripcion']}'" 
                )
        
        
        equipo = db_client.Equipos.find_one({"nombre_equipo": {"$regex": f"^{dato.nombre_equipo}$", "$options": "i"}})
        equipo_oid = equipo["_id"]
        if not equipo:
            raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"El equipo '{dato.nombre_equipo}' no esta cargado" 
                )

        
        if coleccion.find_one({"temporada":temporada_oid, "nombre_equipo": {"$regex": f"^{dato.nombre_equipo}$", "$options": "i"}}):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"El equipo {dato.nombre_equipo} ya esta cargado en la {temporada['descripcion']}")
        
        if not db_client.Equipos.find_one({"nombre_equipo": {"$regex": f"^{dato.nombre_equipo}$", "$options": "i"}}):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                    detail=f"{dato.nombre_equipo} no esta cargado en la base de datos de equipos")
        
        
        
        
        if not db_client.Equipos_por_temporada.find_one({"nombre_equipo":equipo_oid, "temporada":temporada_oid}):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                    detail=f"{dato.nombre_equipo} no esta cargado en esa temporada")
            
        return key
    
