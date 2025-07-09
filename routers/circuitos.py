from fastapi import APIRouter, HTTPException, status
from db.models.circuitos import Circuitos, CircuitosCarga
from db.client import db_client
from db.schemas.circuitos import circuito_schema, circuitos_schema, circuito_carga_schema, circuitos_carga_schema
from bson import ObjectId
from bson.errors import InvalidId
from peticiones_http import peticiones_http_delete, peticiones_http_get, peticiones_http_post, peticiones_http_put
from Validaciones import validar_circuito

router = APIRouter(prefix="/Circuitos",
                   tags=["Circuitos"], 
                   responses={404:{ "message":"No encontrado"}})

def validate_object_id(id: str):
    try:
        return ObjectId(id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="ID inválido")
    
peticiones_http_post.cargar_uno(
    CircuitosCarga,
    router,
    "Circuitos",
    circuito_schema,
    validar_circuito.validar_carga_circuito
)

peticiones_http_post.cargar_muchos(
    CircuitosCarga,
    router,
    "Circuitos",
    circuitos_schema,
    validar_circuito.validar_carga_circuito    
)

@router.get("/", response_model=list[Circuitos])
async def show_circuitos():
    return circuitos_schema(db_client.Circuitos.find())

@router.get("/Buscar/{id}")
async def show_circuito_by_id(id:str):
    try:
        objeto_id = validate_object_id(id)
        return circuito_schema(db_client.circuitos.find_one({"_id":objeto_id}))
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID sin cicuito")
    
@router.get("/Pais/{pais_circuito}")
async def show_circuito_by_pais(pais_circuito:str):
    circuito = circuitos_schema(db_client.circuitos.find({"pais_circuito":pais_circuito}))
    if not circuito:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontraron circuitos de ese pais")
    
    return circuito

@router.get("/Ciudad/{ciudad_circuito}")
async def show_circuito_by_ciudad(ciudad_circuito:str):
    circuito = circuitos_schema(db_client.circuitos.find({"ciudad_circuito":ciudad_circuito}))
    if not circuito:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontraron circuitos de esa ciudad")
    
    return circuito

@router.get("/Cargas", response_model=list[CircuitosCarga])
async def show_teams_for_load():
    circuitos = circuitos_carga_schema(db_client.circuitos.find({"tipo":"Circuito"}))
    return circuitos
        

@router.delete("/Borrar/Todo", status_code=status.HTTP_204_NO_CONTENT)
async def delete_circuito():
    borrado = db_client.circuitos.delete_many({"tipo":"Circuito"})
    if not borrado:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="No se encontro el circuito que se desea eliminar")
    
@router.put("/Modificar", response_model=Circuitos, status_code=status.HTTP_202_ACCEPTED)
async def replace_circuito(circuito:Circuitos):
    try:
        dict_circuito = dict(circuito)
        del dict_circuito["id"]
        dict_circuito["tipo"] = "Circuito"
        
        actualizado = db_client.circuitos.find_one_and_replace({"_id": ObjectId(circuito.id)}, dict_circuito)
        if actualizado:
            return search_data("_id", ObjectId(circuito.id))
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se ah encontrado el circuito")
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se ah modificado el circuito")

def search_data(key:str, value):
    try:
        circuito = db_client.circuitos.find_one({key:value})
        return Circuitos(**circuito_schema(circuito))
        
    except:
        return {"ERROR": "Datos no encontrado"}