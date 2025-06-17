from fastapi import APIRouter, Path,  HTTPException, status
from db.models.pilotos import Piloto, PilotoTemporada
from db.client import db_client
from db.schemas.pilotos import piloto_schema, pilotos_schema, piloto_por_temporada_schema, pilotos_por_temporada_schema
from bson import ObjectId
from bson.errors import InvalidId

router = APIRouter(prefix="/Pilotos_Temporada",
                   tags=["Pilotos por temporada"], 
                   responses={404:{ "message":"No encontrado"}})

def validate_object_id(id: str):
    try:
        return ObjectId(id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="ID inválido")
    
@router.get("/Ver", response_model=list[PilotoTemporada])
async def show_pilotos_for_charge ():
    return pilotos_por_temporada_schema(db_client.pilotos_por_temporada.find())

@router.get("/Ver/Datos/Temporada/{temporada}", response_model=list[PilotoTemporada])
async def show_pilotos_by_category (temporada:str):
    objeto_id = validate_object_id(temporada)
    datas = pilotos_por_temporada_schema(db_client.pilotos_por_temporada.find({"temporada":objeto_id}))
    for data in datas:
        piloto_oid    = ObjectId(data["piloto_participante"])
        piloto = db_client.pilotos.find_one({"_id":piloto_oid})
        
        temporada_oid     = ObjectId(data["temporada"])
        temporada = db_client.temporadas.find_one({"_id":temporada_oid})
        
        data["piloto_participante"] = piloto["piloto_participante"] if piloto else "Desconocido"
        data["temporada"] = temporada["descripcion"] if temporada else "Desconocida"
        
    return datas

@router.get("/Carga/{temporada}")
async def show_pilotos_by_category (temporada:str):
    objeto_id = validate_object_id(temporada)
    lista_pilotos = []
    
    datas = pilotos_por_temporada_schema(db_client.pilotos_por_temporada.find({"temporada":objeto_id}))
    for data in datas:
        piloto_oid    = ObjectId(data["piloto_participante"])
        piloto = db_client.pilotos.find_one({"_id":piloto_oid})
        piloto_nombre = piloto["piloto_participante"] if piloto else "Desconocido"
        dict_pilotos = {
            "piloto_participante": piloto_nombre,
            "temporada": temporada,
            "estado": data.get("estado", "Desconocido")
        }
        lista_pilotos.append(dict_pilotos)
        
    return lista_pilotos
    

@router.post("/Cargar/Uno", response_model=PilotoTemporada, status_code=status.HTTP_201_CREATED)
async def insert_driver_by_id_season(piloto:PilotoTemporada):
    
    busqueda_piloto = buscar_piloto(piloto.piloto_participante)
    dict_piloto = carga_piloto(busqueda_piloto, piloto)
    
    id = db_client.pilotos_por_temporada.insert_one(dict_piloto).inserted_id
    new_piloto = piloto_por_temporada_schema(db_client.pilotos_por_temporada.find_one({"_id":id}))
    
    return PilotoTemporada(**new_piloto)

    
@router.post("/Cargar/Muchos", response_model=list[PilotoTemporada], status_code=status.HTTP_201_CREATED)
async def create_many_pilotos_x_equipos(pilotos:list[PilotoTemporada]):
    
    lista_pilotos = []
    
    for piloto in pilotos:
        if any(c["piloto_participante"] == piloto.piloto_participante for c in pilotos):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Mismo piloto ingresado 2 veces")
        busqueda_piloto = buscar_piloto(piloto.piloto_participante)
        dict_piloto = carga_piloto(busqueda_piloto, piloto)
        lista_pilotos.append(dict_piloto)
    
    resultado = db_client.pilotos_por_temporada.insert_many(lista_pilotos)
    
    ids = resultado.inserted_ids
    documentos = db_client.pilotos_por_temporada.find({"_id":{"$in":ids}})
    
    news_pilotos_por_equipos = pilotos_por_temporada_schema(documentos)
    
    return list(news_pilotos_por_equipos)    

def carga_piloto(busqueda_piloto, piloto):
        if not busqueda_piloto:
            raise HTTPException(status_code=404, detail="El piloto no existe")
    
        try:
            temporada_oid = ObjectId(piloto.temporada)
            piloto_oid    = ObjectId(busqueda_piloto["_id"])
        except:
            raise HTTPException(status_code=400, detail="ID de la temporada invalido")
        filtros = {
            "piloto_participante": piloto_oid,
            "temporada": temporada_oid
        }
    
        if not db_client.temporadas.find_one({"_id": temporada_oid}):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="La temporada ingresada no existe")

        if db_client.pilotos_por_temporada.find_one(filtros):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El piloto ingresado ya se encuentra en esa competicion")
    
        dict_piloto = dict(piloto)
        del dict_piloto["id"]
        dict_piloto["tipo"]                = "Piloto"
        dict_piloto["edad_piloto"]         = busqueda_piloto["edad_piloto"]
        dict_piloto["nacionalidad_piloto"] = busqueda_piloto["nacionalidad_piloto"]
        dict_piloto["piloto_participante"] = piloto_oid
        dict_piloto["temporada"]           = temporada_oid 
        return dict_piloto

def buscar_piloto(piloto_input):
    condiciones = [{"piloto_participante": {"$regex": f"^{piloto_input}$", "$options": "i"}}]
    try:
        condiciones.append({"_id": ObjectId(piloto_input)})
    except:
        pass  # No es un ObjectId, no agregamos esa condición

    return db_client.pilotos.find_one({"$or": condiciones})
    
@router.delete("/Borrar/Todo", status_code=status.HTTP_202_ACCEPTED)
async def delete_pilotos():
        borrado = db_client.pilotos_por_temporada.delete_many({"tipo": "Piloto"})
        if not borrado:
            raise HTTPException(status_code=404, detail="Categoria no encontrado")
