from fastapi import APIRouter, HTTPException, status
from db.models.equipos import Equipos, EquiposPorTemporada
from db.client import db_client
from db.schemas.equipos import equipo_schema, equipos_schema, equipo_historico_schema, equipos_historicos_schema
from bson import ObjectId
from bson.errors import InvalidId
from peticiones_http import peticiones_http_delete, peticiones_http_get, peticiones_http_post,peticiones_http_put
from Validaciones import validar_equipo_por_temporada




router = APIRouter(prefix="/Equipos_Temporada",
                   tags=["Equipos por temporada"], 
                   responses={404:{ "message":"No encontrado"}})


peticiones_http_post.cargar_uno_temporada(
    EquiposPorTemporada,
    router,
    "Equipos_por_temporada",
    equipo_historico_schema,
    validar_equipo_por_temporada.validar_carga_equipo_por_temporada,
    "nombre_equipo"
)

def validate_object_id(id: str):
    try:
        return ObjectId(id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="ID inválido")
    
@router.get("/Ver", response_model=list[EquiposPorTemporada])
async def show_old_teams():
    return equipos_historicos_schema(db_client.equipos_por_temporada.find())

@router.get("/Ver/Datos/Temporada/{temporada}", response_model=list[EquiposPorTemporada])
async def show_pilotos_by_category (temporada:str):
    objeto_id = validate_object_id(temporada)
    datas = equipos_historicos_schema(db_client.equipos_por_temporada.find({"temporada":objeto_id}))
    for data in datas:
        equipo_oid    = ObjectId(data["nombre_equipo"])
        equipo = db_client.equipos.find_one({"_id":equipo_oid})
        
        temporada_oid     = ObjectId(data["temporada"])
        temporada = db_client.temporadas.find_one({"_id":temporada_oid})
        
        data["nombre_equipo"] = equipo["nombre_equipo"] if equipo else "Desconocido"
        data["temporada"] = temporada["descripcion"] if temporada else "Desconocida"
        
    return datas

@router.get("/Carga/{temporada}")
async def show_pilotos_by_category (temporada:str):
    objeto_id = validate_object_id(temporada)
    lista_equipos = []
    
    datas = equipos_historicos_schema(db_client.equipos_por_temporada.find({"temporada":objeto_id}))
    for data in datas:
        equipo_oid    = ObjectId(data["nombre_equipo"])
        equipo = db_client.equipos.find_one({"_id":equipo_oid})
        nombre_equipo = equipo["nombre_equipo"] if equipo else "Desconocido"
        dict_equipos = {
            "nombre_equipo": nombre_equipo,
            "temporada": temporada,
            "estado": data.get("estado", "Desconocido")
        }
        lista_equipos.append(dict_equipos)
        
    return lista_equipos


@router.delete("/Borrar/Todo", status_code=status.HTTP_202_ACCEPTED)
async def delete_old_teams():
    borrado = db_client.equipos_por_temporada.delete_many({"tipo":"Equipo"})
    if not borrado:
        raise HTTPException(status_code=404, detail="")