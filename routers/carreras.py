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



router = APIRouter(prefix="/Carreras",
                   tags=["Carreras"],
                   responses={404:{"Message":"No encontrado"}}
)


def validate_object_id(id: str):
    try:
        return ObjectId(id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="ID inválido")

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
@router.post("/cargar/uno", response_model=DatosTotales, status_code=status.HTTP_201_CREATED)
async def create_carrera(carrera:Carreras):
    
    lista_carrera = []
    lista_puntos_piloto  = []
    lista_puntos_equipo  = []
    
    validacion_carga(carrera)

    dict_puntos_por_piloto,dict_puntos_equipo, dict_carrera = await logica_carga_equipo_piloto(carrera)

    
    id_piloto = db_client.puntos_por_piloto.insert_one(dict_puntos_por_piloto).inserted_id
    new_puntos_por_pilotos = puntos_por_piloto_schema(db_client.puntos_por_piloto.find_one({"_id":id_piloto}))
    

    id_equipo = db_client.puntos_por_equipo.insert_one(dict_puntos_equipo).inserted_id
    new_puntos_por_equipos = puntos_por_equipo_schema(db_client.puntos_por_equipo.find_one({"_id":id_equipo}))
    
    
    id_carrera = db_client.carreras.insert_one(dict_carrera).inserted_id
    new_carrera = carrera_schema(db_client.carreras.find_one({"_id":id_carrera}))
    
    
    lista_carrera = [new_carrera]
    lista_puntos_equipo = [new_puntos_por_equipos]
    lista_puntos_piloto = [new_puntos_por_pilotos] 
    
    
    return DatosTotales(
        carreras=lista_carrera,
        puntos_x_equipo=lista_puntos_equipo,
        puntos_x_piloto=lista_puntos_piloto
    )
    
    

#------------------------------------REALIZAR UNA CARGA---------------------------------------------------#
#------------------------------------REALIZAR MUCHAS CARGA------------------------------------------------#
@router.post("/cargar/muchos", response_model=DatosTotales, status_code=status.HTTP_201_CREATED)
async def create_carreras_one_grand_prix(carreras:list[Carreras]):
    lista_carreras = []
    lista_pilotos  = []
    lista_equipos  = []
    temporada_oid = validate_object_id(carreras[0].temporada)
    for carrera in carreras:
        
        if carrera == carreras[0]:
            ciudad_carrera = carrera.ciudad_circuito
        
        if not ciudad_carrera == carrera.ciudad_circuito:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Las ciudades ingresadas deben ser iguales")
        
        if any(c["posicion"] == carrera.posicion for c in lista_carreras):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Misma posicion ingresada 2 veces {carrera.posicion}")
        
        if any(c["piloto_participante"] == carrera.piloto_participante for c in lista_carreras):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Mismo piloto ingresado 2 veces")

        if sum(c["equipo_participante"] == carrera.equipo_participante for c in lista_carreras) >= 2:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Equipo ingresado mas de 2 veces")
        
        
        await validacion_carga(carrera)
                
        dict_puntos_por_pilotos,dict_puntos_equipos,dict_carreras = await logica_carga_equipo_piloto(carrera)
        
        
        lista_carreras.append(dict_carreras)
        lista_pilotos.append(dict_puntos_por_pilotos)
        lista_equipos.append(dict_puntos_equipos)
            
        
    db_client.carreras.insert_many(lista_carreras)
    db_client.carreras_por_piloto.insert_many(lista_pilotos)
    db_client.carreras_por_equipo.insert_many(lista_equipos)
    
    
    ciudad = carreras[0].ciudad_circuito
    tipo = carreras[0].tipo
    
    new_carreras = carreras_schema(db_client.carreras.find({"ciudad_circuito":ciudad, 
                                                                "tipo":tipo,
                                                                "temporada":temporada_oid}))
    
    new_equipos = puntos_por_equipos_schema(db_client.carreras_por_equipo.find({"ciudad_circuito":ciudad, 
                                                                "tipo":tipo,
                                                                "temporada":temporada_oid}))
    
    new_pilotos = puntos_por_pilotos_schema(db_client.carreras_por_piloto.find({"ciudad_circuito":ciudad, 
                                                                "tipo":tipo,
                                                                "temporada":temporada_oid}))
    
    return DatosTotales(
        carreras=new_carreras,
        puntos_x_equipo=new_equipos,
        puntos_x_piloto=new_pilotos
    )
    
    
async def logica_carga_equipo_piloto(carrera):
    temporada_oid = validate_object_id(carrera.temporada)
    puntos_doc = db_client.sistema_de_puntuacion.find_one({"posicion": carrera.posicion,"tipo":carrera.tipo, "temporada":temporada_oid})
    if puntos_doc:
        puntos = puntos_doc["puntos"]
    else:
        puntos = 0

    
    filtro_piloto={
            "id"                 : "",
            "piloto_participante": carrera.piloto_participante,
            "puntos_piloto"      : puntos,
            "ciudad_circuito"    : carrera.ciudad_circuito,
            "dnf"                : carrera.dnf,
            "temporada"          : temporada_oid,
            "tipo"               : carrera.tipo,
            "estado"             : carrera.estado
        }
    
    dict_puntos_por_pilotos              = dict(filtro_piloto)
    del dict_puntos_por_pilotos["id"]
    dict_puntos_por_pilotos["temporada"] = temporada_oid
    
    filtro_equipo={
            "id"                  : "",
            "equipo_participante" : carrera.equipo_participante,
            "puntos_equipo"       : puntos,
            "ciudad_circuito"     : carrera.ciudad_circuito,
            "temporada"           : temporada_oid,
            "tipo"                : carrera.tipo,
            "estado"              : carrera.estado
        }
        
    dict_puntos_equipos              = dict(filtro_equipo)
    del dict_puntos_equipos["id"]
    dict_puntos_equipos["temporada"] = temporada_oid
        
    dict_carrera              = dict(carrera)
    del dict_carrera["id"]    
    dict_carrera["temporada"] = temporada_oid
        
    return dict_puntos_por_pilotos, dict_puntos_equipos, dict_carrera

    
async def validacion_carga(carrera):
    temporada_oid = validate_object_id(carrera.temporada)
    temporada = db_client.temporadas.find_one({"_id":temporada_oid})
    filtro = {
        "piloto_participante": carrera.piloto_participante,
        "ciudad_circuito"    : carrera.ciudad_circuito,
        "temporada"          : temporada_oid,
        "tipo"               : carrera.tipo
        }
    
    if db_client.carreras.find_one(filtro) :
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Datos existentes")
    
        
    if not db_client.pilotos.find_one({"piloto_participante":carrera.piloto_participante}):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"El piloto {carrera.piloto_participante} ingresado no esta en la base de datos")
    
    
    if not db_client.equipos.find_one({"nombre_equipo": {"$regex": f"^{carrera.equipo_participante}$", "$options": "i"}}):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El equipo ingresado no esta en la base de datos")

    if not db_client.ConformacionDeEquipos.find_one({
            "$or": [
                {"primer_piloto": {"$regex": f"^{carrera.piloto_participante}$", "$options": "i"}},
                {"segundo_piloto": {"$regex": f"^{carrera.piloto_participante}$", "$options": "i"}},
                {"piloto_reserva": {"$regex": f"^{carrera.piloto_participante}$", "$options": "i"}},
                {"otro_piloto": {"$regex": f"^{carrera.piloto_participante}$", "$options": "i"}},
                {"otro_piloto_dos": {"$regex": f"^{carrera.piloto_participante}$", "$options": "i"}}
            ],
            "nombre_equipo": {"$regex": f"^{carrera.equipo_participante}$", "$options": "i"}
        }): raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El piloto no está en ese equipo")
    
    if not db_client.sistema_de_puntuacion.find_one({"tipo":carrera.tipo, "temporada":temporada_oid}):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"La temporada '{temporada["descripcion"]}' no cuenta con el tipo de carrera {carrera.tipo}")
    
    if db_client.carreras.find_one({"piloto_participante":carrera.piloto_participante, "ciudad_circuito":carrera.ciudad_circuito, "temporada":temporada_oid,  "tipo":carrera.tipo }):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El piloto ingresado ya existe en esa carrera")

    if db_client.puntos_por_equipo.count_documents({"equipo_participante":carrera.equipo_participante, "ciudad_circuito":carrera.ciudad_circuito, "temporada":temporada_oid,"tipo":carrera.tipo}) == 2:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"El equipo {carrera.equipo_participante} esta completo en ese carrera")
    
    if db_client.carreras.find_one({"ciudad_circuito":carrera.ciudad_circuito,"temporada":temporada_oid, "posicion": carrera.posicion,"tipo":carrera.tipo}):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="La posicion ingresada de esa carrera ya existe")
    
    if not db_client.circuitos.find_one({"ciudad_circuito":carrera.ciudad_circuito}):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El circuito ingresado no existe")
        
    if not db_client.circuitos_por_temporada.find_one({"ciudad_circuito":carrera.ciudad_circuito, "temporada":temporada_oid}):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El circuito ingresado no esta cargado en esa temporada")
    
    return carrera

                
                
                

                
                
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

