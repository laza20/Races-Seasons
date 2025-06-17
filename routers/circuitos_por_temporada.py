from fastapi import APIRouter, HTTPException, status
from db.models.circuitos import CircuitosPorTemporada, CircuitosPorTemporadaCarga
from db.client import db_client
from db.schemas.circuitos import circuito_por_temporada_schema, circuitos_por_temporada_schema, circuito_carga_por_temporada_schema, circuitos_por_temporada_carga_schema
from db.schemas.temporada import temporada_schema, temporadas_schema
from bson import ObjectId
from bson.errors import InvalidId

router = APIRouter(prefix="/Circuitos_Temporada",
                   tags=["Circuitos por temporada"], 
                   responses={404:{ "message":"No encontrado"}})

def validate_object_id(id: str):
    try:
        return ObjectId(id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="ID inválido")
    
@router.get("/Ver", response_model=list[CircuitosPorTemporada])
async def show_pilotos():
    return circuitos_por_temporada_schema(db_client.circuitos_por_temporada.find())

@router.get("/Cargas/{categoria}/{year}")
async def show_teams_for_load(categoria:str, year:int):
    lista_circuitos=[]
    temporada = temporada_schema(db_client.temporadas.find_one({"year":year,"categoria":categoria}))
    if not temporada:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="temporada incorrecta")
    temporada_id = temporada["_id"]
    temporada_oid = validate_object_id(temporada_id)
    circuitos = circuitos_por_temporada_schema(db_client.circuitos_por_temporada.find({"temporada":temporada_oid}))
    for circuito in circuitos:
        dict_circuito={
            "circuito":circuito["ciudad_circuito"],
            "temporada":str(temporada_oid),
            "estado":circuito["estado"]
        }
        lista_circuitos.append(dict_circuito)
        
    return lista_circuitos


@router.post("/Cargar/Uno", response_model=CircuitosPorTemporada, status_code=status.HTTP_201_CREATED)
async def create_grand_prix_for_season(circuito:CircuitosPorTemporada):
    try:
        temporada_oid = ObjectId(circuito.temporada)
    except:
        raise HTTPException(status_code=400, detail="ID de la temporada no válido")
    
    temporada_actual = db_client.temporadas.find_one({"_id": temporada_oid})
    if not temporada_actual:
        raise HTTPException(status_code=404, detail="Temporada no encontrada")
    
    if db_client.circuitos_por_temporada.count_documents({"temporada":temporada_oid}) >= temporada_actual["cantidad_de_grandes_premios"]:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Temporada con todos los grandes premios ingresados")
    
    busqueda_circuito = buscar_circuito(circuito.circuito)
    dict_circuito = cargar_circuito(busqueda_circuito, circuito)
    
    id = db_client.circuitos_por_temporada.insert_one(dict_circuito).inserted_id
    new_circuito = circuito_por_temporada_schema(db_client.circuitos_por_temporada.find_one({"_id":id}))
    
    return CircuitosPorTemporada(**new_circuito)

@router.post("/Cargar/Muchos", response_model=list[CircuitosPorTemporada], status_code=status.HTTP_201_CREATED)
async def create_many_circuitos(circuitos:list[CircuitosPorTemporada]):
    lista_circuitos = []
    try:
        temporada_oid = ObjectId(circuitos[0].temporada)
    except:
        raise HTTPException(status_code=400, detail="ID de la temporada no válido")

    temporada_actual = db_client.temporadas.find_one({"_id": temporada_oid})
    if not temporada_actual:
        raise HTTPException(status_code=404, detail="Temporada no encontrada")

    cantidad_actual = db_client.circuitos_por_temporada.count_documents({"temporada": temporada_oid})

    cantidad_maxima = temporada_actual.get("cantidad_de_grandes_premios")
    if not isinstance(cantidad_maxima, int):
        raise HTTPException(status_code=500, detail="El campo 'cantidad_de_grandes_premios' no está bien definido en la temporada")

    if cantidad_actual + len(circuitos) > cantidad_maxima:
        raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=f"No se pueden agregar {len(circuitos)} circuitos: la temporada ya tiene {cantidad_actual}/{cantidad_maxima}"
        )
    for circuito in circuitos:
        busqueda_circuito = buscar_circuito(circuito.circuito)
        dict_circuito = cargar_circuito(busqueda_circuito, circuito)
        lista_circuitos.append(dict_circuito)
        
    
    resultado = db_client.circuitos_por_temporada.insert_many(lista_circuitos)
    
    circuitos_ids = resultado.inserted_ids
    documentos = db_client.circuitos_por_temporada.find({"_id":{"$in": circuitos_ids }})
    
    news_circuitos = circuitos_por_temporada_schema(documentos)
    
    return list(news_circuitos)

def cargar_circuito(busqueda_circuito, circuito):
        if not busqueda_circuito:
            raise HTTPException(status_code=404, detail="El circuito no existe")
        try:
            temporada_oid = ObjectId(circuito.temporada)
            circuito_oid    = ObjectId(busqueda_circuito["_id"])
        except:
            raise HTTPException(status_code=400, detail="ID de la temporada no válido")
        filtros = {
        "temporada": temporada_oid,
        "circuito" : circuito_oid
        } 
        
        if db_client.circuitos_por_temporada.find_one(filtros):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"El circuito {circuito.ciudad_circuito} coincidente a uno existente en la temporada")
    
        if not db_client.circuitos.find_one({"_id":circuito_oid}):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El circuito no esta en la base de datos de circuitos")
    
   
        
        dict_circuito = dict(circuito)
        del dict_circuito["id"]
        dict_circuito["circuito"]  = circuito_oid
        dict_circuito["pais_circuito"] = busqueda_circuito["pais_circuito"]
        dict_circuito["ciudad_circuito"] = busqueda_circuito["ciudad_circuito"]
        dict_circuito["distancia_del_circuito"] = busqueda_circuito["distancia_del_circuito"]
        dict_circuito["temporada"] = temporada_oid
        dict_circuito["tipo"] = "Circuito"
        return dict_circuito


def buscar_circuito(circuito_input):
    condiciones = [{"ciudad_circuito": {"$regex": f"^{circuito_input}$", "$options": "i"}}]
    try:
        condiciones.append({"_id": ObjectId(circuito_input)})
    except:
        pass  # No es un ObjectId, no agregamos esa condición

    return db_client.circuitos.find_one({"$or": condiciones})

@router.delete("/Borrar/Todo", status_code=status.HTTP_202_ACCEPTED)
async def delete_old_circuit():
    borrado = db_client.circuitos_por_temporada.delete_many({"tipo":"Circuito"})
    if not borrado:
        raise HTTPException(status_code=404, detail="")