from fastapi import APIRouter, HTTPException, status
from db.models.circuitos import CircuitosPorTemporada, CircuitosPorTemporadaCarga
from db.client import db_client
from db.schemas.circuitos import circuito_por_temporada_schema, circuitos_por_temporada_schema, circuito_carga_por_temporada_schema, circuitos_por_temporada_carga_schema
from db.schemas.temporada import temporada_schema, temporadas_schema
from bson import ObjectId
from bson.errors import InvalidId
from peticiones_http import peticiones_http_delete, peticiones_http_get, peticiones_http_post, peticiones_http_put
from Validaciones import validar_circuito_por_temporada

router = APIRouter(prefix="/Circuitos_Temporada",
                   tags=["Circuitos por temporada"], 
                   responses={404:{ "message":"No encontrado"}})

peticiones_http_post.cargar_uno_temporada(
    CircuitosPorTemporadaCarga,
    router,
    "Circuitos_por_temporada",
    circuito_por_temporada_schema,
    validar_circuito_por_temporada.validar_carga_circuito_por_temporada,
    "ciudad_circuito"
)

peticiones_http_post.cargar_muchos_temporada(
    CircuitosPorTemporadaCarga,
    router,
    "Circuitos_por_temporada",
    circuitos_por_temporada_schema,
    validar_circuito_por_temporada.validar_carga_circuito_por_temporada,
    "ciudad_circuito"
)

peticiones_http_get.view_old_data(
    router, 
    "Circuitos_por_temporada", 
    CircuitosPorTemporada, 
    circuitos_por_temporada_schema
)

peticiones_http_get.view_data_by_id(
    router, 
    "Circuitos_por_temporada", 
    CircuitosPorTemporada, 
    circuito_por_temporada_schema
)

peticiones_http_get.view_data_for_season_by_category_and_year(
    router,
    "ciudad_circuito", 
    "Circuitos_por_temporada", 
    circuito_por_temporada_schema,
    "Circuitos"
    )



def validate_object_id(id: str):
    try:
        return ObjectId(id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="ID inválido")
    


@router.delete("/Borrar/Todo", status_code=status.HTTP_202_ACCEPTED)
async def delete_old_circuit():
    borrado = db_client.Circuitos_por_temporada.delete_many({"tipo":"Circuitos_por_temporada"})
    if not borrado:
        raise HTTPException(status_code=404, detail="")