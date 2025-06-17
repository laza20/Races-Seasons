from fastapi import APIRouter, HTTPException, status, Path
from db.client import db_client
from bson import ObjectId
from bson.errors import InvalidId
from db.models.puntos_por_equipos import PuntosXEquipo
from db.models.puntos_por_pilotos import PuntosXPiloto
from db.models.realizar_carreras import Carreras
from db.models.carrera_todos_los_datos import DatosTotales
from db.models.podios import PodiosPorEquipo, PodiosPorEquipoTemporada,PodiosPorPilotoTemporada, PodiosPorPilotoTotal
from db.schemas.carreras_todos_los_datos import carrera_todos_los_datos_schema_una_carrera, carrera_todos_los_datos_schema_todas_las_carrera
from db.schemas.realizar_carreras import carrera_schema , carreras_schema
from db.schemas.puntos_por_equipos import puntos_por_equipo_schema, puntos_por_equipos_schema
from db.schemas.puntos_por_piloto import puntos_por_piloto_schema, puntos_por_pilotos_schema
from db.schemas.sistema_de_puntuacion import punto_schema, puntos_schema
from db.schemas.temporada import temporada_schema, temporadas_schema
from db.schemas.pilotos import piloto_por_temporada_schema, piloto_schema,pilotos_por_temporada_schema,pilotos_schema


router = APIRouter(prefix="/Datos/Carreras",
                   tags=["Datos de Carreras"],
                   responses={404:{"Message":"No encontrado"}}
)


def validate_object_id(id: str):
    try:
        return ObjectId(id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="ID inválido")


@router.get("/Totales/{temporada}",  response_model=DatosTotales)
async def obtener_datos_totales(temporada:str):
        temporada_oid = validate_object_id(temporada)
        todas_las_carreras_de_una_temporada = list(db_client.carreras.find(
            {"temporada":temporada_oid}))
        
        todas_las_carreras_de_un_piloto_temporada = list(db_client.carreras_por_piloto.find(
            {"temporada":temporada_oid}))
        
        todas_las_carreras_de_un_equipo_temporada = list(db_client.carreras_por_equipo.find(
            {"temporada":temporada_oid}))

        
        lista_carrera, lista_puntos_equipo, lista_puntos_piloto = [], [], []
        
        for carrera, piloto, equipo in zip(todas_las_carreras_de_una_temporada, todas_las_carreras_de_un_piloto_temporada,todas_las_carreras_de_un_equipo_temporada):
            datos_carrera, datos_equipo, datos_piloto = carrera_todos_los_datos_schema_una_carrera(carrera, piloto, equipo)
            lista_carrera.append(datos_carrera)
            lista_puntos_equipo.append(datos_equipo)
            lista_puntos_piloto.append(datos_piloto)
            
        return  DatosTotales(
            carreras=lista_carrera,
            puntos_x_equipo=lista_puntos_equipo,
            puntos_x_piloto=lista_puntos_piloto
    )
        
@router.get("/Ciudad/{temporada}/{ciudad_circuito}", response_model=list[Carreras])
async def show_carreras(ciudad_circuito: str, temporada:str):
    temporada_oid = validate_object_id(temporada)
    carreras = carreras_schema(db_client.carreras.find({"ciudad_circuito":ciudad_circuito, 
                                                        "temporada": temporada_oid}))
    if not carreras:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontraron carreras")
    
    return carreras


@router.get("/Equipos/Puntos/Totales", response_model=list[PuntosXEquipo])
async def show_equipos_en_carreras():
    equipos = puntos_por_equipos_schema(db_client.carreras_por_equipo.find())
    if not equipos:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontraron equipos")
    
    return equipos

@router.get("/Pilotos/Puntos/Totales", response_model=list[PuntosXPiloto])
async def show_pilotos_en_carreras():
    pilotos = puntos_por_pilotos_schema(db_client.carreras_por_piloto.find())
    if not pilotos:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontraron pilotos")
    
    return pilotos


@router.get("/Carreras/{id}")
async def show_carrera_by_id(id=str):
    try:
        object_id = validate_object_id(id)
        return carrera_schema(db_client.carreras.find_one({"_id":object_id}))
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID carrera")

@router.get("/Circuito/Pilotos/{temporada}/{ciudad_circuito}/{tipo}", response_model=list[PuntosXPiloto])
async def show_carrera_by_city_and_year(ciudad_circuito: str, temporada:str, tipo:str):
    temporada_oid = validate_object_id(temporada)
    pilotos = puntos_por_pilotos_schema(db_client.carreras_por_piloto.find({"ciudad_circuito":ciudad_circuito, 
                                                                          "temporada":temporada_oid, 
                                                                          "tipo":tipo}))
    
    posicion = sorted(pilotos, key=lambda c: c["puntos_piloto"], reverse=True)
    return posicion



@router.get("/Piloto/Podios/Temporada/{piloto_participante}/{temporada}", response_model=PodiosPorPilotoTemporada)
async def show_podiums_for_drivers(piloto_participante:str, temporada:str):
    temporada_oid = validate_object_id(temporada)
    piloto = await buscar_piloto(piloto_participante, temporada_oid)
    carreras_totales = puntos_por_pilotos_schema(db_client.carreras_por_piloto.find({
        "piloto_participante":{"$regex": f"^{piloto_participante}$", "$options": "i"},
        "temporada":temporada_oid
    }))
    
    puntos_por_posicion = puntos_schema(db_client.sistema_de_puntuacion.find({"temporada":temporada_oid}))
            
    primer_lugar, segundo_lugar, tercer_lugar, podios = await buscar_podios_pilotos(carreras_totales, puntos_por_posicion)
                
    podios_piloto = await transformacion_piloto(podios, piloto, primer_lugar, segundo_lugar, tercer_lugar, piloto_participante, temporada_oid)
    return podios_piloto
            

@router.get("/Piloto/Podios/Totales/{piloto_participante}/{categoria}", response_model=PodiosPorPilotoTotal)
async def show_podiums_for_drivers(piloto_participante:str, categoria:str):
    temporadas = list(db_client.temporadas.find({"categoria":categoria}))
    piloto = db_client.pilotos.find_one({"piloto_participante":piloto_participante})
    primer_lugar = 0
    segundo_lugar = 0
    tercer_lugar = 0
    podios = 0
    for temporada in temporadas:
        id = temporada["_id"]
        carreras_por_año = puntos_por_pilotos_schema(db_client.carreras_por_piloto.find({
        "piloto_participante":{"$regex": f"^{piloto_participante}$", "$options": "i"},
        "temporada" : id
        }))
        puntos_por_posicion = puntos_schema(db_client.sistema_de_puntuacion.find({"temporada":id}))
        primer_lugar_temp, segundo_lugar_temp, tercer_lugar_temp, podios_temp = await buscar_podios_pilotos(carreras_por_año, puntos_por_posicion)
        primer_lugar  += primer_lugar_temp
        segundo_lugar += segundo_lugar_temp
        tercer_lugar  += tercer_lugar_temp
        
    
    podios=primer_lugar+segundo_lugar+tercer_lugar
    podios_piloto = {
        "nombre_piloto"         : piloto_participante,
        "nacionalidad_piloto"   : piloto["nacionalidad_piloto"],
        "edad_piloto"           : piloto["edad_piloto"],
        "podios_piloto"         : podios,
        "primer_lugar"          : primer_lugar,
        "segundo_lugar"         : segundo_lugar,
        "tercer_lugar"          : tercer_lugar,
            }
        
    return podios_piloto


@router.get("/Equipos/Podios/Circuitos/Año/{equipo_participante}/{year}/{categoria}", response_model=PodiosPorEquipo)
async def show_podiums_for_drivers(equipo_participante:str, year:int, categoria:str):
    
    equipo = await buscar_equipo(equipo_participante)
    
    carreras_totales = puntos_por_equipos_schema(db_client.puntos_por_equipo.find({
        "equipo_participante":{"$regex": f"^{equipo_participante}$", "$options": "i"},
        "year": year,
        "categoria":categoria
    }))
    
    puntos_por_posicion = puntos_schema(db_client.puntosxposicion.find({"categoria":categoria}))
            
    primer_lugar, segundo_lugar, tercer_lugar, podios = await buscar_podios(carreras_totales, puntos_por_posicion)

    podios_equipo = await transformacion_equipo(podios, primer_lugar, segundo_lugar, tercer_lugar, equipo)
    
    return podios_equipo



@router.get("/Equipos/Podios/Totales/{equipo_participante}/{categoria}", response_model=PodiosPorEquipo)
async def show_podiums_for_drivers(equipo_participante:str, categoria:str):

    equipo = await buscar_equipo(equipo_participante)
    
    carreras_totales = puntos_por_equipos_schema(db_client.puntos_por_equipo.find({
        "equipo_participante":{"$regex": f"^{equipo_participante}$", "$options": "i"},
        "categoria":categoria
    }))
    
    puntos_por_posicion = puntos_schema(db_client.puntosxposicion.find({"categoria":categoria}))
    
    primer_lugar, segundo_lugar, tercer_lugar, podios = await buscar_podios(carreras_totales, puntos_por_posicion)
    
    podios_equipo = await transformacion_equipo(podios, primer_lugar, segundo_lugar, tercer_lugar, equipo)

    
    return podios_equipo

async def buscar_podios_equipos(carreras_totales, puntos_por_posicion):
    primer_lugar = 0
    segundo_lugar = 0
    tercer_lugar = 0
    for carrera in carreras_totales:
        tipo_carrera = carrera["tipo"]
        for puntos in puntos_por_posicion:
            if carrera["puntos_equipo"] == puntos["puntos"] and tipo_carrera == puntos["tipo"]:
                if puntos["posicion"] == 3:
                    tercer_lugar += 1
                elif puntos["posicion"] == 2:
                    segundo_lugar += 1
                elif puntos["posicion"] == 1:
                    primer_lugar += 1
                    
    podios = primer_lugar + segundo_lugar + tercer_lugar
    return primer_lugar, segundo_lugar, tercer_lugar, podios
    
async def buscar_podios_pilotos(carreras_totales, puntos_por_posicion):
    primer_lugar = 0
    segundo_lugar = 0
    tercer_lugar = 0
    for carrera in carreras_totales:
        tipo_carrera = carrera["tipo"]
        for puntos in puntos_por_posicion:
            if carrera["puntos_piloto"] == puntos["puntos"] and tipo_carrera == puntos["tipo"]:
                if puntos["posicion"] == 3:
                    tercer_lugar += 1
                elif puntos["posicion"] == 2:
                    segundo_lugar += 1
                elif puntos["posicion"] == 1:
                    primer_lugar += 1
                    
    podios = primer_lugar + segundo_lugar + tercer_lugar
    return primer_lugar, segundo_lugar, tercer_lugar, podios
    
async def buscar_piloto(piloto, temporada_oid):
    piloto_encontrado = db_client.pilotos.find_one({"piloto_participante":piloto})
    id = piloto_encontrado["_id"]
    piloto_participante = validate_object_id(id)
    piloto = db_client.pilotos_por_temporada.find_one({
        "piloto_participante":piloto_participante,
        "temporada" : temporada_oid
    })
    if not piloto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Piloto no encontrado en la temporada")
    
    return piloto

async def buscar_equipo(equipo_participante):
    equipo = db_client.equipos.find_one({
        "nombre_equipo": {"$regex": f"^{equipo_participante}$", "$options": "i"}
    })
    if not equipo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Equipo no encontrado")
    return equipo
    
async def transformacion_equipo(podios, primer_lugar, segundo_lugar, tercer_lugar, equipo):
    podios_equipo = {}
    podios_equipo = {
        "nombre_equipo"         : equipo["nombre_equipo"],
        "nacionalidad_equipo"   : equipo["pais_equipo"],
        "podios_equipo"         : podios,
        "primer_lugar"          : primer_lugar,
        "segundo_lugar"         : segundo_lugar,
        "tercer_lugar"          : tercer_lugar,
        "categoria"             : equipo["categoria"]
            }
    return podios_equipo

async def transformacion_piloto(podios, piloto, primer_lugar, segundo_lugar, tercer_lugar, piloto_participante, temporada_oid):
    podios_piloto = {}
    temporada_actual = db_client.temporadas.find_one({"_id":temporada_oid})
    podios_piloto = {
        "nombre_piloto"         : piloto_participante,
        "nacionalidad_piloto"   : piloto["nacionalidad_piloto"],
        "edad_piloto"           : piloto["edad_piloto"],
        "podios_piloto"         : podios,
        "primer_lugar"          : primer_lugar,
        "segundo_lugar"         : segundo_lugar,
        "tercer_lugar"          : tercer_lugar,
        "temporada"             : temporada_actual["descripcion"]
            }
    
    return podios_piloto
    
def search_data(key:str, value, base_datos, schema, Objeto):
    try:
        data = base_datos.find_one({key:value})
        return Objeto(**schema(data))
    except:
        return {"ERROR": "Datos no encontrado"}