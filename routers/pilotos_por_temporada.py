from fastapi import APIRouter, Path,  HTTPException, status
from db.models.pilotos import Piloto, PilotoTemporada
from db.client import db_client
from db.schemas.pilotos import piloto_schema, pilotos_schema, piloto_por_temporada_schema, pilotos_por_temporada_schema
from bson import ObjectId
from bson.errors import InvalidId
from peticiones_http import peticiones_http_delete, peticiones_http_get, peticiones_http_post, peticiones_http_put
from Validaciones import validar_pilotos_por_temporada

router = APIRouter(prefix="/Pilotos_Temporada",
                   tags=["Pilotos por temporada"], 
                   responses={404:{ "message":"No encontrado"}})


peticiones_http_post.cargar_uno_temporada(
    PilotoTemporada,
    router,
    "Pilotos_por_temporada",
    piloto_por_temporada_schema,
    validar_pilotos_por_temporada.validar_carga_piloto_por_temporada,
    "piloto_participante"
)

peticiones_http_post.cargar_muchos_temporada(
    PilotoTemporada,
    router,
    "Pilotos_por_temporada",
    pilotos_por_temporada_schema,
    validar_pilotos_por_temporada.validar_carga_piloto_por_temporada,
    "piloto_participante"
)

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
    
@router.delete("/Borrar/Todo", status_code=status.HTTP_202_ACCEPTED)
async def delete_pilotos():
        borrado = db_client.pilotos_por_temporada.delete_many({"tipo": "Piloto"})
        if not borrado:
            raise HTTPException(status_code=404, detail="Categoria no encontrado")
