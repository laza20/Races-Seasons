from fastapi import APIRouter, HTTPException, status
from db.models.equipos import Equipos, EquiposPorTemporada
from db.client import db_client
from db.schemas.equipos import equipo_schema, equipos_schema, equipo_historico_schema, equipos_historicos_schema
from bson import ObjectId
from bson.errors import InvalidId




router = APIRouter(prefix="/Equipos_Temporada",
                   tags=["Equipos por temporada"], 
                   responses={404:{ "message":"No encontrado"}})

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



@router.post("/Cargar/Uno", response_model=EquiposPorTemporada, status_code=status.HTTP_201_CREATED)
async def insert_team_season(equipo:EquiposPorTemporada):
    try:
        temporada_oid = ObjectId(equipo.temporada)
    except:
        raise HTTPException(status_code=400, detail="ID de la temporada no válido")

    temporada_actual = db_client.temporadas.find_one({"_id": temporada_oid})
    if not temporada_actual:
        raise HTTPException(status_code=404, detail="Temporada no encontrada")
    
    if db_client.equipos_por_temporada.count_documents({"temporada":temporada_oid}) >= temporada_actual["cantidad_de_equipos"]:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Temporada con todos los equipos ingresados")
     
    busqueda_equipo = buscar_equipo(equipo.nombre_equipo)
    dict_equipo = carga_equipo(busqueda_equipo, equipo)
    id = db_client.equipos_por_temporada.insert_one(dict_equipo).inserted_id
    new_equipo = equipo_historico_schema(db_client.equipos_por_temporada.find_one({"_id":id}))
    
    return EquiposPorTemporada(**new_equipo)

@router.post("/Cargar/Muchos", response_model=list[EquiposPorTemporada], status_code=status.HTTP_201_CREATED)
async def insert_many_teams_season(equipos:list[EquiposPorTemporada]):
    lista_equipos = []
    try:
        temporada_oid = ObjectId(equipos[0].temporada)
    except:
        raise HTTPException(status_code=400, detail="ID de la temporada no válido")

    temporada_actual = db_client.temporadas.find_one({"_id": temporada_oid})
    if not temporada_actual:
        raise HTTPException(status_code=404, detail="Temporada no encontrada")

    cantidad_actual = db_client.equipos_por_temporada.count_documents({"temporada": temporada_oid})

    if cantidad_actual + len(equipos) > temporada_actual["cantidad_de_equipos"]:
        raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=f"No se pueden agregar {len(equipos)} equipos: la temporada ya tiene {cantidad_actual}/{temporada_actual['cantidad_de_equipos']}"
        )
        
    for equipo in equipos:
        if any(c["nombre_equipo"] == equipo.nombre_equipo for c in equipos):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Mismo equipo ingresado 2 veces")
        
        busqueda_equipo = buscar_equipo(equipo.nombre_equipo)
        dict_equipo = carga_equipo(busqueda_equipo, equipo)
        lista_equipos.append(dict_equipo)
        
    resultado = db_client.equipos_por_temporada.insert_many(lista_equipos)
    
    ids = resultado.inserted_ids
    documentos = db_client.equipos_por_temporada.find({"_id":{"$in": ids }})
    
    news_equipos = equipos_historicos_schema(documentos)
    
    return list(news_equipos)

def carga_equipo(busqueda_equipo, equipo):
        if not busqueda_equipo:
            raise HTTPException(status_code=404, detail="El equipo no existe")
    
        try:
            temporada_oid = ObjectId(equipo.temporada)
            equipo_oid    = ObjectId(busqueda_equipo["_id"])
        except:
            raise HTTPException(status_code=400, detail="ID de la temporada invalido")
        filtros = {
            "nombre_equipo" : {"$regex": f"^{equipo.nombre_equipo}$", "$options": "i"},
            "pais_equipo"   : {"$regex": f"^{equipo.pais_equipo}$", "$options": "i"},
            "temporada"     : equipo.temporada
        }

        if db_client.equipos_por_temporada.find_one(filtros):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El equipo ingresado ya se encuentra en esa competicion")
    
        if not db_client.equipos.find_one({"_id":equipo_oid}):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El equipo no esta en la base de datos de equipos")
    
        dict_equipo = dict(equipo)
        del dict_equipo["id"]
        dict_equipo["nombre_equipo"]       = equipo_oid
        dict_equipo["pais_equipo"]         = busqueda_equipo["pais_equipo"]
        dict_equipo["tipo"]                = "Equipo"
        dict_equipo["temporada"]           = temporada_oid 
        return dict_equipo

def buscar_equipo(equipo_input):
    condiciones = [{"nombre_equipo": {"$regex": f"^{equipo_input}$", "$options": "i"}}]
    try:
        condiciones.append({"_id": ObjectId(equipo_input)})
    except:
        pass  # No es un ObjectId, no agregamos esa condición

    return db_client.equipos.find_one({"$or": condiciones})


@router.delete("/Borrar/Todo", status_code=status.HTTP_202_ACCEPTED)
async def delete_old_teams():
    borrado = db_client.equipos_por_temporada.delete_many({"tipo":"Equipo"})
    if not borrado:
        raise HTTPException(status_code=404, detail="")