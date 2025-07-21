from fastapi import APIRouter, HTTPException, status,Path
from db.client import db_client
from bson import ObjectId
from bson.errors import InvalidId
from db.models.carreras import Carreras, CarrerasCarga
from db.models.carrera_todos_los_datos import DatosTotales
from db.schemas.carreras import carrera_schema , carreras_schema
from db.schemas.puntos_por_equipos import puntos_por_equipo_schema, puntos_por_equipos_schema
from db.schemas.puntos_por_piloto import puntos_por_piloto_schema, puntos_por_pilotos_schema
from db.schemas.temporada import temporada_schema, temporadas_schema
from peticiones_http import peticiones_http_delete, peticiones_http_get, peticiones_http_post, peticiones_http_put
from Validaciones import validar_carreras_por_temporada



router = APIRouter(prefix="/Carreras",
                   tags=["Carreras"],
                   responses={404:{"Message":"No encontrado"}}
)


def validate_object_id(id: str):
    try:
        return ObjectId(id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="ID inválido")
    
peticiones_http_post.cargar_uno_carrera(
    Carreras,  
    router,
    "Carreras",
    "",
    validar_carreras_por_temporada.validar_carga_carrera_por_temporada
) 


@router.get("/Carga/{ciudad_circuito}/{year}/{categoria}/{tipo}", response_model=list[CarrerasCarga])
async def show_race_for_load (categoria:str, year:int, ciudad_circuito:str, tipo:str):
    temporada = db_client.temporadas.find_one({"categoria":categoria, "year":year})
    id = temporada["_id"]
    temporada_oid = validate_object_id(id)
    datas = carreras_schema(db_client.carreras.find({"temporada":temporada_oid, 
                                                     "ciudad_circuito":ciudad_circuito, 
                                                     "tipo":tipo}))
    
    posiciones = sorted(datas, key=lambda c: c["posicion"])
        
    return posiciones

        

    

#------------------------------------REALIZAR UNA CARGA---------------------------------------------------#
#------------------------------------REALIZAR MUCHAS CARGA------------------------------------------------#

    


                
                
                

                
                
@router.delete("/Borrar/Todo/{temporada}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_race_by_year(temporada:str):
    temporada = validate_object_id(temporada)
    borrado = db_client.carreras.delete_many({"temporada":temporada})
    borrado = db_client.carreras_por_equipo.delete_many({"temporada":temporada})
    borrado = db_client.carreras_por_piloto.delete_many({"temporada":temporada})         

    if not borrado:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="No se encontro el año que se desea eliminar")
    
    
    
@router.delete("/borrar/carrera/{ciudad_circuito}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_circuito(ciudad_circuito:str):
    borrado = db_client.carreras.delete_many({"ciudad_circuito":ciudad_circuito})
    borrado = db_client.puntos_por_equipo.delete_many({"ciudad_circuito":ciudad_circuito})
    borrado = db_client.puntos_por_piloto.delete_many({"ciudad_circuito":ciudad_circuito})
    
    if not borrado:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="No se encontro el circuito que se desea eliminar")
    
@router.delete("/borrar/carreras/tipo/{ciudad_circuito}/{tipo}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_circuito(ciudad_circuito:str, tipo:str):
    borrado = db_client.carreras.delete_many({"ciudad_circuito":ciudad_circuito, "tipo":tipo})
    borrado = db_client.puntos_por_equipo.delete_many({"ciudad_circuito":ciudad_circuito, "tipo":tipo})
    borrado = db_client.puntos_por_piloto.delete_many({"ciudad_circuito":ciudad_circuito, "tipo":tipo})
    
    if not borrado:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="No se encontro el circuito que se desea eliminar")

