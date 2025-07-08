from fastapi import APIRouter, HTTPException, status
from db.models.circuitos import CircuitosPorTemporada, CircuitosPorTemporadaCarga
from db.client import db_client
from db.schemas.circuitos import circuito_por_temporada_schema, circuitos_por_temporada_schema, circuito_carga_por_temporada_schema, circuitos_por_temporada_carga_schema
from db.schemas.temporada import temporada_schema, temporadas_schema
from bson import ObjectId
from bson.errors import InvalidId
from funciones import peticiones_http_delete, peticiones_http_get, peticiones_http_post, peticiones_http_put, validaciones

router = APIRouter(prefix="/Circuitos_Temporada",
                   tags=["Circuitos por temporada"], 
                   responses={404:{ "message":"No encontrado"}})

peticiones_http_post.cargar_uno_temporada(
    CircuitosPorTemporadaCarga,
    router,
    "Circuitos_por_temporada",
    circuito_por_temporada_schema,
    validaciones.validar_carga_circuito_por_temporada,
    "ciudad_circuito"
)

peticiones_http_post.cargar_muchos_temporada(
    CircuitosPorTemporadaCarga,
    router,
    "Circuitos_por_temporada",
    circuitos_por_temporada_schema,
    validaciones.validar_carga_circuito_por_temporada,
    "ciudad_circuito"
)

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


@router.delete("/Borrar/Todo", status_code=status.HTTP_202_ACCEPTED)
async def delete_old_circuit():
    borrado = db_client.Circuitos_por_temporada.delete_many({"tipo":"Circuitos_por_temporada"})
    if not borrado:
        raise HTTPException(status_code=404, detail="")