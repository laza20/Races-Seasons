from fastapi import APIRouter, HTTPException, status,Path
from db.client import db_client
from bson import ObjectId
from bson.errors import InvalidId
from db.models.Tabla_posicion_campeonato import TablaPosicionCampeonato, TablaPosicionesCircuito
from db.schemas.equipos import equipo_schema, equipos_schema
from db.schemas.puntos_por_equipos import puntos_por_equipo_schema, puntos_por_equipos_schema
from db.schemas.pilotos import pilotos_schema, piloto_schema, piloto_por_temporada_schema, pilotos_por_temporada_schema
from db.schemas.puntos_por_piloto import puntos_por_piloto_schema, puntos_por_pilotos_schema
from db.schemas.sistema_de_puntuacion import punto_schema, puntos_schema


router = APIRouter(prefix="/Posiciones",
                   tags=["Posiciones"],
                   responses={404:{"Message":"No encontrado"}}
)

def validate_id(id):
    try:
        return ObjectId(id)
    except:
        raise HTTPException(status_code=400, detail="ID inválido")

@router.get("/Equipos/{categoria}/{year}", response_model=list[TablaPosicionCampeonato])
async def show_table_positions_teams(year:int, categoria:str):
    temporada = db_client.temporadas.find_one({"categoria":categoria, "year":year})
    temporada_id = temporada["_id"]
    temporada_oid = validate_id(temporada_id)
    try:
        equipos = equipos_schema(db_client.equipos_por_temporada.find({"temporada":temporada_oid}))
        if not equipos:
            raise HTTPException(status_code=404, detail="No equipos found")
        tabla_posiciones = []
        for equipo in equipos:

            id = equipo["nombre_equipo"]
            equipo_id = validate_id(id)
            team = db_client.equipos.find_one({"_id":equipo_id})
            nombre_equipo = team["nombre_equipo"]
            carreras_de_un_equipo = puntos_por_equipos_schema(
            db_client.carreras_por_equipo.find({
                "equipo_participante": {"$regex": f"^{nombre_equipo}$", "$options": "i"},
                "temporada":temporada_oid
            }))
            cantidad_carreras = db_client.carreras_por_equipo.count_documents({
                "equipo_participante": {"$regex": f"^{nombre_equipo}$", "$options": "i"},
                "temporada":temporada_oid
            })
            
            puntos_totales = sum(carrera["puntos_equipo"] for carrera in carreras_de_un_equipo)
            
            tabla_posiciones.append({
                "nombre"              : nombre_equipo,
                "puntos"              : puntos_totales,
                "cantidad_de_carreras":cantidad_carreras,
                "temporada"           : temporada["descripcion"],
                "year"                : year,
                "categoria"           : categoria
            })
        
            
        posiciones = sorted(tabla_posiciones, key=lambda c: c["puntos"], reverse=True)
        posiciones_nuevas = sorted(posiciones, key=lambda c: c["cantidad_de_carreras"], reverse=True)
        for i , posicion in enumerate(posiciones_nuevas, start=1):
            posicion["posicion"] = i
        return posiciones
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/Pilotos/{categoria}/{year}", response_model=list[TablaPosicionCampeonato])
async def show_table_positions_pilotos(year:int, categoria:str):
    temporada = db_client.temporadas.find_one({"categoria":categoria, "year":year})
    temporada_id = temporada["_id"]
    temporada_oid = validate_id(temporada_id)
    try:
        pilotos = pilotos_por_temporada_schema(db_client.pilotos_por_temporada.find({"temporada":temporada_oid}))
        if not pilotos:
            raise HTTPException(status_code=404, detail="No pilotos found")
        tabla_posiciones = []
        for piloto in pilotos:
            id = piloto["piloto_participante"]
            piloto_id = validate_id(id)
            driver = db_client.pilotos.find_one({"_id":piloto_id})
            piloto_participante = driver["piloto_participante"]
            carreras_de_un_piloto = puntos_por_pilotos_schema(
                db_client.carreras_por_piloto.find({
                "piloto_participante": {"$regex": f"^{piloto_participante}$", "$options": "i"},
                "temporada":temporada_oid
            }))
            cantidad_carreras = db_client.carreras_por_piloto.count_documents({
                "piloto_participante": {"$regex": f"^{piloto_participante}$", "$options": "i"},
                "temporada":temporada_oid
            })
            
            puntos_totales = sum(carrera["puntos_piloto"] for carrera in carreras_de_un_piloto)
            
            tabla_posiciones.append(
                {
                "nombre"   : piloto_participante,
                "puntos"   : puntos_totales,
                "cantidad_de_carreras":cantidad_carreras,
                "temporada": temporada["descripcion"],
                "year"     : year,
                "categoria": categoria
            })

        posiciones = sorted(tabla_posiciones, key=lambda c: c["puntos"], reverse=True)
        posiciones_nuevas = sorted(posiciones, key=lambda c: c["cantidad_de_carreras"], reverse=True)
        posiciones_filtradas = [p for p in posiciones_nuevas if p["cantidad_de_carreras"] > 0]
        for i , posicion in enumerate(posiciones_filtradas, start=1):
            posicion["posicion"] = i
            
            
        return posiciones_filtradas
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/Circuito/Equipos/{categoria}/{ciudad_circuito}/{tipo}/{year}", response_model=list[TablaPosicionesCircuito])
async def show_position_teams_race_by_city_and_year(categoria:str,ciudad_circuito: str, tipo:str,year:int):
    temporada = db_client.temporadas.find_one({"categoria":categoria, "year":year})
    temporada_id = temporada["_id"]
    temporada_oid = validate_id(temporada_id)
    if not db_client.carreras_por_equipo.find_one({"temporada":temporada_oid,
                                                 "ciudad_circuito":{"$regex": f"^{ciudad_circuito}$", "$options": "i"},
                                                 "tipo":tipo}):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="url incorrecta")
    
    equipos = equipos_schema(db_client.equipos_por_temporada.find({"temporada":temporada_oid}))
    
    posiciones=[]
    
    for equipo in equipos:
        id = equipo["nombre_equipo"]
        equipo_id = validate_id(id)
        team = db_client.equipos.find_one({"_id":equipo_id})
        nombre_equipo = team["nombre_equipo"]
        carreras_de_un_equipo = puntos_por_equipos_schema(db_client.carreras_por_equipo.find({
            "equipo_participante": {"$regex": f"^{nombre_equipo}$", "$options": "i"},
            "temporada":temporada_oid,
            "ciudad_circuito":{"$regex": f"^{ciudad_circuito}$", "$options": "i"},
            "tipo":tipo}))
        puntos_de_equipo = sum(carrera["puntos_equipo"] for carrera in carreras_de_un_equipo)
        posiciones.append({
                "nombre"              : nombre_equipo,
                "puntos"              : puntos_de_equipo,
                "circuito"            : ciudad_circuito ,
                "temporada"           : temporada["descripcion"],
                "year"                : year,
                "categoria"           : categoria
            })
        
    posiciones_en_la_carrera = sorted(posiciones, key=lambda c: c["puntos"], reverse=True)
    for i , posicion in enumerate(posiciones_en_la_carrera, start=1):
        posicion["posicion"] = i
    return posiciones_en_la_carrera


@router.get("/Circuito/Pilotos/{categoria}/{ciudad_circuito}/{tipo}/{year}", response_model=list[TablaPosicionesCircuito])
async def show_position_drivers_race_by_city_and_year(categoria:str,ciudad_circuito: str, tipo:str,year:int):
    temporada = db_client.temporadas.find_one({"categoria":categoria, "year":year})
    temporada_id = temporada["_id"]
    temporada_oid = validate_id(temporada_id)   
    carreras = db_client.carreras.find({"temporada":temporada_oid, 
                                               "tipo":tipo, 
                                               "ciudad_circuito":ciudad_circuito})
    posiciones=[]
    for carrera in carreras:
        piloto_participante = carrera["piloto_participante"]
        posicion = carrera["posicion"]
        punto_doc = db_client.sistema_de_puntuacion.find_one({"temporada":temporada_oid,"tipo":tipo,"posicion":posicion})
        if punto_doc:
            puntos_de_piloto = punto_schema(punto_doc)
        else:
            puntos_de_piloto = {"puntos": 0}
        posiciones.append({
                "nombre"   : piloto_participante,
                "puntos"   : puntos_de_piloto["puntos"],
                "circuito" : ciudad_circuito,
                "temporada": temporada["descripcion"],
                "year"     : year,
                "categoria": categoria
            })
        
    posiciones_en_la_carrera = sorted(posiciones, key=lambda c: c["puntos"], reverse=True)
    for i , posicion in enumerate(posiciones_en_la_carrera, start=1):
            posicion["posicion"] = i
    return posiciones_en_la_carrera

