from db.client import db_client
from errores import errores_simples
from funciones import funciones_logicas
from fastapi import HTTPException, status


def transformacion(base_de_datos, podios, dict_dato, primer_lugar, segundo_lugar, tercer_lugar, dato, temporada_oid):
    if base_de_datos ==  "Carreras_por_pilotos":
        podios =   transformacion_piloto(podios, dict_dato, primer_lugar, segundo_lugar, tercer_lugar, dato, temporada_oid)
    else:
        podios =  transformacion_equipo(podios, dict_dato, primer_lugar, segundo_lugar, tercer_lugar, dato, temporada_oid)
        
    return podios




def transformacion_equipo(podios, equipo, primer_lugar, segundo_lugar, tercer_lugar, dato, temporada_oid):
    podios_equipo = {}
    temporada_actual = db_client.Temporadas.find_one({"_id": temporada_oid})
    podios_equipo = {
        "nombre_equipo": dato,
        "nacionalidad_equipo": equipo["pais_equipo"],
        "podios_equipo": podios,
        "primer_lugar": primer_lugar,
        "segundo_lugar": segundo_lugar,
        "tercer_lugar": tercer_lugar,
        "categoria"             : temporada_actual["categoria"],
        "año"                   : temporada_actual["year"],
        "temporada"             : temporada_actual["descripcion"]
    }
    return podios_equipo

def transformacion_piloto(podios, piloto, primer_lugar, segundo_lugar, tercer_lugar, dato, temporada_oid):
    podios_piloto = {}
    temporada_actual = db_client.Temporadas.find_one({"_id":temporada_oid})
    podios_piloto = {
        "nombre_piloto"         : dato,
        "nacionalidad_piloto"   : piloto["nacionalidad_piloto"],
        "edad_piloto"           : piloto["edad_piloto"],
        "podios_piloto"         : podios,
        "primer_lugar"          : primer_lugar,
        "segundo_lugar"         : segundo_lugar,
        "tercer_lugar"          : tercer_lugar,
        "categoria"             : temporada_actual["categoria"],
        "año"                   : temporada_actual["year"],
        "temporada"             : temporada_actual["descripcion"]
            }
    
    return podios_piloto

def buscar_podios(carreras_totales, puntos_por_posicion, base_de_datos):
    if base_de_datos == "Carreras_por_pilotos":
        campo = "puntos_piloto"
    else:
        campo = "puntos_equipo"
        
    primer_lugar = 0
    segundo_lugar = 0
    tercer_lugar = 0
    for carrera in carreras_totales:
        tipo_carrera = carrera["tipo_carrera"]
        for puntos in puntos_por_posicion:
            if carrera[campo] == puntos["puntos"] and tipo_carrera == puntos["tipo_carrera"]:
                if puntos["posicion"] == 3:
                    tercer_lugar += 1
                elif puntos["posicion"] == 2:
                    segundo_lugar += 1
                elif puntos["posicion"] == 1:
                    primer_lugar += 1
                    
    podios = primer_lugar + segundo_lugar + tercer_lugar
    return primer_lugar, segundo_lugar, tercer_lugar, podios


def buscar_data_team_or_driver(base_de_datos, dato, temporada_oid):
    coleccion_uno, coleccion_dos, campo, campo_carrera =  seleccionar_piloto_o_equipo(base_de_datos)
    dato_encontrado = coleccion_dos.find_one({campo:dato}) #busca en la base de datos de pilotos o equipos
    if not dato_encontrado:
        errores_simples.error_sin_documentos_en_la_base_de_datos(dato, base_de_datos)
        
    id = dato_encontrado["_id"]
    dato_participante = funciones_logicas.validate_object_id(id)
    participante = coleccion_uno.find_one({ #busca en la base de datos de pilotos_por_temporada o equipos_por_temporada
        campo       : dato_participante,
        "temporada" : temporada_oid
    })
    if not participante:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Piloto {dato}, {campo} no encontrado en la temporada")
    
    return participante,campo_carrera

def seleccionar_piloto_o_equipo(base_de_datos):
    if base_de_datos == "Carreras_por_pilotos":
        coleccion_uno = getattr(db_client, "Pilotos_por_temporada")
        coleccion_dos = getattr(db_client, "Pilotos")
        campo = "piloto_participante"
        campo_carrera = "piloto_participante"
    else:
        coleccion_uno = getattr(db_client, "Equipos_por_temporada")
        coleccion_dos = getattr(db_client, "Equipos")
        campo = "nombre_equipo"
        campo_carrera = "equipo_participante"
        
    return coleccion_uno, coleccion_dos, campo, campo_carrera