from fastapi import APIRouter, HTTPException, status
import re
from db.client import db_client
from db.models.conformacion_de_equipos import ConformacionDeEquipos, ConformacionDeEquiposCarga
from db.schemas.conformacion_de_equipos import piloto_x_equipo_schema, pilotos_x_equipos_schema
from bson import ObjectId
from bson.errors import InvalidId

router = APIRouter( prefix="/Conformacion_equipos",
                   tags=["Conformacion de equipos"],
                   responses={404:{ "message":"No encontrado"}})

def validate_object_id(id: str):
    try:
        return ObjectId(id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="ID inválido")


@router.get("/", response_model=list[ConformacionDeEquipos])
async def show_pilotos_x_equipos():
    return pilotos_x_equipos_schema(db_client.ConformacionDeEquipos.find())

@router.get("/Ver/{id}")
async def show_piloto_x_equipo(id:str):
    try:
        object_id = validate_object_id(id)
        return piloto_x_equipo_schema(db_client.ConformacionDeEquipos.find_one({"_id":object_id}))
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID sin equipo")
    
@router.get("/Ver/Datos/Temporada/{temporada}", response_model=list[ConformacionDeEquipos])
async def show_pilotos_by_category (temporada:str):
    objeto_id = validate_object_id(temporada)
    datas = pilotos_x_equipos_schema(db_client.ConformacionDeEquipos.find({"temporada":objeto_id}))
    for data in datas:  
        temporada_oid     = ObjectId(data["temporada"])
        temporada = db_client.temporadas.find_one({"_id":temporada_oid})
        data["temporada"] = temporada["descripcion"] if temporada else "Desconocida"
        
    return datas 

@router.get("/Carga/{temporada}", response_model=list[ConformacionDeEquiposCarga])
async def show_teams_by_load (temporada:str):
    objeto_id = validate_object_id(temporada)
    datas = pilotos_x_equipos_schema(db_client.ConformacionDeEquipos.find({"temporada":objeto_id}))

    return datas


    

@router.post("/Cargar/Uno", response_model=ConformacionDeEquipos, status_code=status.HTTP_201_CREATED)
def create_pilotos_x_equipos(pilotos_x_equipos:ConformacionDeEquipos):
    dict_pilotos_x_equipos= realizar_carga(pilotos_x_equipos)
           
    id = db_client.ConformacionDeEquipos.insert_one(dict_pilotos_x_equipos).inserted_id
    new_equipo_x_piloto = piloto_x_equipo_schema(db_client.ConformacionDeEquipos.find_one({"_id":id}))
   
    return ConformacionDeEquipos(**new_equipo_x_piloto)

    
    
    
@router.post("/Cargar/Muchos", response_model=list[ConformacionDeEquipos], status_code=status.HTTP_201_CREATED)
async def create_many_pilotos_x_equipos(pilotos_x_equipos:list[ConformacionDeEquipos]):
    
    lista_pilotos_x_equipos = []
    
    for conformacion in pilotos_x_equipos:
        if any(c["nombre_equipo"] == conformacion.nombre_equipo for c in pilotos_x_equipos):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Mismo equipo ingresado 2 veces")
        
        
        dict_pilotos_x_equipos= realizar_carga(conformacion)
        lista_pilotos_x_equipos.append(dict_pilotos_x_equipos)
    
    resultado = db_client.ConformacionDeEquipos.insert_many(lista_pilotos_x_equipos)
    ids = resultado.inserted_ids
    documentos = db_client.ConformacionDeEquipos.find({"_id":{"$in":ids}})
    news_pilotos_por_equipos = pilotos_x_equipos_schema(documentos)
    
    return list(news_pilotos_por_equipos)

def realizar_carga(conformacion):
        try:
            temporada_oid = ObjectId(conformacion.temporada)
        except:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID de la temporada no válido")
    
        temporada = db_client.temporadas.find_one({"_id":temporada_oid})
        buscar_pilotos = {}
        if conformacion.primer_piloto and conformacion.segundo_piloto: 
            buscar_pilotos["primer_piloto"] = conformacion.primer_piloto.strip()
            buscar_pilotos["segundo_piloto"] = conformacion.segundo_piloto.strip()
        else:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                    detail="El primer y segundo piloto deben estar cargados")
        if conformacion.piloto_reserva:
            buscar_pilotos["piloto_reserva"] = conformacion.piloto_reserva.strip()
        if conformacion.otro_piloto:
            buscar_pilotos["otro_piloto"] = conformacion.otro_piloto.strip()
        if conformacion.otro_piloto_dos:
            buscar_pilotos["otro_piloto_dos"] = conformacion.otro_piloto_dos.strip()
        
        for key, nombre in buscar_pilotos.items():
            if not nombre:
                nombre = "Null"
                continue
        
            piloto = db_client.pilotos.find_one({"piloto_participante": {"$regex": f"^{nombre}$", "$options": "i"}})
            
        
            if not piloto:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"El piloto '{nombre}' en el campo '{key}' no existe en la BD de pilotos" 
                )
            piloto_oid = piloto["_id"]
            piloto_en_la_temporada = db_client.pilotos_por_temporada.find_one({
                "piloto_participante": piloto_oid,
                "temporada": temporada_oid
                })
            if not piloto_en_la_temporada:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"El piloto '{nombre}' en el campo '{key}' no esta cargado en la temporada '{temporada['descripcion']}'" 
                )
        
        equipo = db_client.equipos.find_one({"nombre_equipo": {"$regex": f"^{conformacion.nombre_equipo}$", "$options": "i"}})
        if not equipo:
            raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"El equipo '{conformacion.nombre_equipo}' no esta cargado" 
                )
        equipo_oid = ObjectId(equipo["_id"])
        datos = {
            "temporada": temporada_oid,
            "nombre_equipo": equipo_oid
        }
        
        if db_client.ConformacionDeEquipos.find_one({"temporada":temporada_oid, "nombre_equipo": {"$regex": f"^{conformacion.nombre_equipo}$", "$options": "i"}}):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"El equipo {conformacion.nombre_equipo} ya esta cargado en la {temporada['descripcion']}")
        
        if not db_client.equipos.find_one({"nombre_equipo":conformacion.nombre_equipo}):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                    detail=f"{conformacion.nombre_equipo} no esta cargado en la base de datos de equipos")
        
        if not db_client.equipos_por_temporada.find_one(datos):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                    detail=f"{conformacion.nombre_equipo} no esta cargado en esa temporada")
        
        dict_pilotos_x_equipos = dict(conformacion)
        del dict_pilotos_x_equipos["id"]
        dict_pilotos_x_equipos["tipo"] = "Formacion"
        dict_pilotos_x_equipos["temporada"] = temporada_oid
        return dict_pilotos_x_equipos

    
    

def search_data(key:str, value):
    try:
        piloto_x_equipo = db_client.ConformacionDeEquipos.find_one({key:value})
        return ConformacionDeEquipos(**piloto_x_equipo_schema(piloto_x_equipo))
    except:
        {"ERROR":"Datos no encontrados"}
