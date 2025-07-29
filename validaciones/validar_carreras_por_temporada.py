from db.client import db_client
from fastapi import HTTPException, status
from funciones import funciones_logicas
from collections import defaultdict
from validaciones_generales import validaciones_generales_simples, validaciones_generales_dobles
        
def validar_carga_carrera_por_temporada(datos, base_de_datos):
    if isinstance(datos, list) and len(datos) >= 2:
        carreras = set()
        pilotos  = set() 
        equipos = defaultdict(int)
        ciudad  = defaultdict(int)
        for dato in datos:
            temporada_oid, max_posicion, temporada = validar_carga_carrera_por_temporada_2(dato)
            validacion_de_carga_repetida(dato, carreras, pilotos, equipos, ciudad, temporada_oid, max_posicion, temporada)
    else:
        dato = datos if not isinstance(datos, list) else datos[0]
        temporada_oid, max_posicion, temporada = validar_carga_carrera_por_temporada_2(dato)

#Funcion para evitar la duplicidad de la carga de documentos de circuitos por temporada
def validar_carga_carrera_por_temporada_2(dato):
        temporada_oid = funciones_logicas.validate_object_id(dato.temporada)
        
        temporada, piloto = encontrar_datos(dato, temporada_oid)
        validaciones_simples(dato, piloto)
        validaciones_dobles(dato, temporada_oid)
        validacion_cuadruple(dato, temporada_oid, temporada)
        max_posicion = validar_posicion_maxima_de_la_temporada(dato, temporada)
        validar_conformacion_de_equipo(dato)

        return temporada_oid, max_posicion, temporada


def validacion_de_carga_repetida(dato, carreras, pilotos, equipos, ciudad, temporada_oid, max_posicion, temporada):
        key_carrera = (temporada_oid, dato.ciudad_circuito, dato.posicion, dato.tipo_carrera)
        key_piloto  = (temporada_oid, dato.piloto_participante, dato.tipo_carrera, dato.ciudad_circuito)
        key_equipos = (temporada_oid, dato.equipo_participante, dato.ciudad_circuito, dato.tipo_carrera)
        key_ciudad  = (temporada_oid, dato.ciudad_circuito, dato.tipo_carrera)

        if key_carrera in carreras:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"La entrega fue enviada con una duplicacion de datos para la (posicion = '{dato.posicion}'), en la (temporada = '{temporada['descripcion']}') para la carrera '{dato.tipo_carrera}' de la ciudad = '{dato.ciudad_circuito}'."
            )
        carreras.add(key_carrera)
        
        if key_piloto in pilotos:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"El piloto {dato.piloto_participante} fue ingresado mas de una vez en la entrega de datos para la carrera en la ciudad = '{dato.ciudad_circuito}', de la temporada = '{temporada['descripcion']} con el tipo de carrera '{dato.tipo_carrera}'."
            )
        pilotos.add(key_piloto)
        
        ciudad[key_ciudad] += 1
        if ciudad[key_ciudad] > max_posicion:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Para la ciudad = '{dato.ciudad_circuito}' en el tipo de carrera = '{dato.tipo_carrera}' de la temporada = '{temporada['descripcion']} ya se cargaron todas las posiciones"
            )
            
        equipos[key_equipos] += 1
        if equipos[key_equipos] > max_posicion:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"El equipo {dato.equipo_participante} ingresado mas de 2 veces para una carrera"
            )



def encontrar_datos(dato, temporada_oid):
        temporada = db_client.Temporadas.find_one({"_id":temporada_oid})
        piloto = db_client.Pilotos.find_one({"piloto_participante":dato.piloto_participante})
        return temporada, piloto
    
    
def validaciones_simples(dato, piloto):
    validaciones_generales_simples.validacion_simple_general_negativa("Pilotos_por_temporada", piloto["_id"])
    
    validaciones_generales_simples.validacion_simple_general_negativa("Pilotos", dato.piloto_participante)
    
    validaciones_generales_simples.validacion_simple_general_negativa("Equipos", dato.equipo_participante)
    
    validaciones_generales_simples.validacion_simple_general_negativa("Circuitos", dato.ciudad_circuito)
        
def validaciones_dobles(dato, temporada_oid):
    #negativa
    validaciones_generales_dobles.validacion_doble_negativa_general("Circuitos_por_temporada", dato.ciudad_circuito, temporada_oid)
    #negativa
    validaciones_generales_dobles.validacion_doble_negativa_general("Sistema_de_puntuacion", temporada_oid, dato.tipo_carrera)
    
def validacion_cuadruple(dato, temporada_oid, temporada):
    filtro = {
    "piloto_participante": {"$regex": f"^{dato.piloto_participante}$", "$options": "i"},
    "ciudad_circuito"    : {"$regex": f"^{dato.ciudad_circuito}$", "$options": "i"},
    "temporada"          : temporada_oid,
    "tipo_carrera"       : {"$regex": f"^{dato.tipo_carrera}$", "$options": "i"}
    }
    
    if db_client.Carreras.find_one(filtro) :
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"La carrera de la ciudad = '{dato.ciudad_circuito}', en la temporada ('{temporada['descripcion']}' con id = '{temporada_oid}') ya cuenta con el datos sobre el piloto = '{dato.piloto_participante}' para el tipo de carrera = '{dato.tipo_carrera}'")
    
    if db_client.Puntos_por_equipo.count_documents({"equipo_participante":dato.equipo_participante, "ciudad_circuito":dato.ciudad_circuito, "temporada":temporada_oid,"tipo_carrera":dato.tipo_carrera}) == 2:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"El equipo {dato.equipo_participante} esta completo en ese carrera")

    if db_client.Carreras.find_one({"ciudad_circuito":dato.ciudad_circuito,"temporada":temporada_oid, "posicion": dato.posicion,"tipo_carrera":dato.tipo_carrera}):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"La posicion = '{dato.posicion}', en la carrera de la ciudad '{dato.ciudad_circuito}' para la temporada = '{temporada['descripcion']}' y el tipo de carrera = '{dato.tipo_carrera}'  ya existe.")


def validar_posicion_maxima_de_la_temporada(dato, temporada):
    max_posicion = temporada["cantidad_de_equipos"] * 2
    
    if dato.posicion > max_posicion:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"La temporada '{temporada['descripcion']}' no tiene posiciones mas alla de {max_posicion} y el usuario ingreso {dato.posicion}")
    
    return max_posicion

def validar_conformacion_de_equipo(dato):
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
