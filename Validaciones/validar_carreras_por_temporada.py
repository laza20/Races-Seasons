from db.client import db_client
from fastapi import HTTPException, status
from funciones import funciones_logicas

        
def validar_carga_carrera_por_temporada(datos, base_de_datos):
    coleccion = getattr(db_client, base_de_datos)
    if isinstance(datos, list) and len(datos) >= 2:
        carreras = set()
        for dato in datos:
            key = validar_carga_carrera_por_temporada_2(dato)
            if key in carreras:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Carrera duplicada en la entrega"
                )
            carreras.add(key)
    else:
        dato = datos if not isinstance(datos, list) else datos[0]
        validar_carga_carrera_por_temporada_2(dato)

#Funcion para evitar la duplicidad de la carga de documentos de circuitos por temporada
def validar_carga_carrera_por_temporada_2(dato):
        temporada_oid = funciones_logicas.validate_object_id(dato.temporada)
        temporada = db_client.Temporadas.find_one({"_id":temporada_oid})
        filtro = {
            "piloto_participante": dato.piloto_participante,
            "ciudad_circuito"    : dato.ciudad_circuito,
            "temporada"          : temporada_oid,
            "tipo"               : dato.tipo_carrera
            }

        if db_client.Carreras.find_one(filtro) :
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Datos existentes")

            
        if not db_client.Pilotos.find_one({"piloto_participante":dato.piloto_participante}):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"El piloto {dato.piloto_participante} ingresado no esta en la base de datos")


        if not db_client.Equipos.find_one({"nombre_equipo": {"$regex": f"^{dato.equipo_participante}$", "$options": "i"}}):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El equipo ingresado no esta en la base de datos")

        if not db_client.Conformacion_de_equipos.find_one({
                "$or": [
                    {"primer_piloto": {"$regex": f"^{dato.piloto_participante}$", "$options": "i"}},
                    {"segundo_piloto": {"$regex": f"^{dato.piloto_participante}$", "$options": "i"}},
                    {"piloto_reserva": {"$regex": f"^{dato.piloto_participante}$", "$options": "i"}},
                    {"otro_piloto": {"$regex": f"^{dato.piloto_participante}$", "$options": "i"}},
                    {"otro_piloto_dos": {"$regex": f"^{dato.piloto_participante}$", "$options": "i"}}
                ],
                "nombre_equipo": {"$regex": f"^{dato.equipo_participante}$", "$options": "i"}
            }): raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"El piloto {dato.piloto_participante} no está en ese equipo")

        if not db_client.Sistema_de_puntuacion.find_one({"tipo_carrera":dato.tipo_carrera, "temporada":temporada_oid}):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"La temporada '{temporada["descripcion"]}' no cuenta con el tipo de carrera {dato.tipo_carrera}")

        if db_client.Carreras.find_one({"piloto_participante":dato.piloto_participante, "ciudad_circuito":dato.ciudad_circuito, "temporada":temporada_oid,  "tipo":dato.tipo_carrera }):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El piloto ingresado ya existe en esa carrera")

        if db_client.Puntos_por_equipo.count_documents({"equipo_participante":dato.equipo_participante, "ciudad_circuito":dato.ciudad_circuito, "temporada":temporada_oid,"tipo":dato.tipo_carrera}) == 2:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"El equipo {dato.equipo_participante} esta completo en ese carrera")

        if db_client.Carreras.find_one({"ciudad_circuito":dato.ciudad_circuito,"temporada":temporada_oid, "posicion": dato.posicion,"tipo":dato.tipo_carrera}):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="La posicion ingresada de esa carrera ya existe")

        if not db_client.Circuitos.find_one({"ciudad_circuito":dato.ciudad_circuito}):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El circuito ingresado no existe")
            
        if not db_client.Circuitos_por_temporada.find_one({"ciudad_circuito":dato.ciudad_circuito, "temporada":temporada_oid}):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El circuito ingresado no esta cargado en esa temporada")

        
        
