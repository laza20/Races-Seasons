from db.client import db_client
from errores import errores_simples
from funciones import funciones_logicas
from fastapi import HTTPException, status

def transformacion_total(base_de_datos, podios, primer_lugar, segundo_lugar, tercer_lugar, dato, temporada_oid):
    if base_de_datos ==  "Carreras_por_pilotos":
        podios =   transformacion_pilotos_total(podios, primer_lugar, segundo_lugar, tercer_lugar, dato, temporada_oid)
    else:
        podios =   transformacion_equipos_total(podios, primer_lugar, segundo_lugar, tercer_lugar, dato, temporada_oid)
        
    return podios

def transformacion_temporada(base_de_datos, podios, dict_dato, primer_lugar, segundo_lugar, tercer_lugar, dato, temporada_oid):
    if base_de_datos ==  "Carreras_por_pilotos":
            podios =   transformacion_piloto_temporada(podios, dict_dato, primer_lugar, segundo_lugar, tercer_lugar, dato, temporada_oid)
    else:
        podios =  transformacion_equipo_temporada(podios, dict_dato, primer_lugar, segundo_lugar, tercer_lugar, dato, temporada_oid)
    return podios

def inicializar_podios_totales():
        podiums_totales = 0
        podiums_primero = 0
        podiums_segundo = 0
        podiums_tercero = 0 
        return podiums_totales, podiums_primero, podiums_segundo, podiums_tercero



def transformacion_equipos_total(podios, primer_lugar, segundo_lugar, tercer_lugar, dato, categoria):
    podios_equipo = {}
    podios_equipo = {
        "nombre_equipo"         : dato,
        "podios_equipo"         : podios,
        "primer_lugar"          : primer_lugar,
        "segundo_lugar"         : segundo_lugar,
        "tercer_lugar"          : tercer_lugar,
        "categoria"             : categoria
    }
    return podios_equipo

def transformacion_pilotos_total(podios, primer_lugar, segundo_lugar, tercer_lugar, dato, categoria):
    podios_piloto = {}
    podios_piloto = {
        "nombre_piloto"         : dato,
        "podios_piloto"         : podios,
        "primer_lugar"          : primer_lugar,
        "segundo_lugar"         : segundo_lugar,
        "tercer_lugar"          : tercer_lugar,
        "categoria"             : categoria
            }
    
    return podios_piloto


def transformacion_equipo_temporada(podios, equipo, primer_lugar, segundo_lugar, tercer_lugar, dato, temporada_oid):
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

def transformacion_piloto_temporada(podios, piloto, primer_lugar, segundo_lugar, tercer_lugar, dato, temporada_oid):
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


#retorna el el campo_carrera el cual sera utilizado para verificar si un piloto o equipo estan
#dentro de la base de datos de carreras_por_piloto o carreras_por_equipo, ademas retorna un dict del piloto o equipo
#que puede ser usado para sacar la informacion de este
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
    
    #retorna el dict de pilotos o equipos por temporada y el campo que servira para verificar los datos.
    return participante, campo_carrera


#el piloto_participante y nombre_equipo en pilotos_por_temporada y equipos_por_temporada
#son ids por eso esta funcion se encarga de buscar esos ids y retornarlos como nombres para poder usarlos
#en la verificacion. lo hace por medio del nombre (tanto del equipo como del piloto)
def buscar_id_piloto_o_equipo(base_de_datos, dato):
    if base_de_datos == "Carreras_por_pilotos":
        piloto = db_client.Pilotos.find_one({"piloto_participante":{"$regex": f"^{dato}$", "$options": "i"}})
        if not piloto:
            errores_simples.error_sin_documentos_en_la_base_de_datos(dato, base_de_datos)
        dato_oid = funciones_logicas.validate_object_id(piloto["_id"])
    else:
        equipo = db_client.Equipos.find_one({"nombre_equipo":{"$regex": f"^{dato}$", "$options": "i"}})
        if not equipo:
            errores_simples.error_sin_documentos_en_la_base_de_datos(dato, base_de_datos)
        dato_oid = funciones_logicas.validate_object_id(equipo["_id"])
    
    return dato_oid

#verifica si un dato esta en la temporada que se envie.
def verificar_existencia_dato_en_temporada(base_de_datos, dato_oid, temporada_oid):
    if base_de_datos == "Carreras_por_pilotos":
        piloto = db_client.Pilotos_por_temporada.find_one({"piloto_participante":dato_oid,
                                                            "temporada": temporada_oid})
        if not piloto:
            return "false"
    else:
        equipo = db_client.Equipos_por_temporada.find_one({"nombre_equipo":dato_oid,
                                                            "temporada": temporada_oid})
        if not equipo:
            return "false"

#dependiende la base de datos selecciona una serie de campos.
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