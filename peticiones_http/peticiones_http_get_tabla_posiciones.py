#pyright: reportInvalidTypeForm=false
from funciones import funciones_logicas
from fastapi import status
from db.client import db_client
from funciones import funciones_logicas
from fastapi import  HTTPException, status
from errores import errores_simples
from db.models.Tabla_posicion_campeonato import TablaPosicionCampeonato, TablaPosicionesCircuito
from db.schemas.equipos import equipo_schema, equipos_schema
from validaciones_generales import lista_de_campos
from db.schemas.puntos_por_equipos import puntos_por_equipo_schema, puntos_por_equipos_schema
from db.schemas.pilotos import pilotos_schema, piloto_schema, piloto_por_temporada_schema, pilotos_por_temporada_schema
from db.schemas.puntos_por_piloto import puntos_por_piloto_schema, puntos_por_pilotos_schema
from db.schemas.equipos import equipos_schema, equipos_historicos_schema
from db.schemas.sistema_de_puntuacion import punto_schema, puntos_schema
from funciones import funciones_busqueda
from funciones import funciones_podios

def view_positions_teams_for_year_and_category(router, base_de_datos, schema):
    @router.get("/Posiciones/Categoria/{categoria}/Año/{year}", response_model=list[TablaPosicionCampeonato])
    async def show_table_positions_teams(year:int, categoria:str):
        coleccion = formar_colecciones(base_de_datos)
        temporada_oid = retornar_temporada_oid_por_categoria_y_año(categoria, year)
        if not temporada_oid:
            errores_simples.error_sin_documentos_en_la_base_de_datos(f"{categoria}-{year}", "Temporadas")
        temporada = funciones_busqueda.encontrar_un_documento(temporada_oid, "Temporadas")
        
        campo_equipo_o_piloto, campo_carrera, puntos = busqueda_campos(base_de_datos)
            

        try:
            base_de_datos_por_temporada, base_de_datos_equipos_o_pilotos, schema_dos, schema_tres = buscar_datos_por_temporada(base_de_datos)
            if base_de_datos_por_temporada != "false":
                coleccion_dos  = formar_colecciones(base_de_datos_por_temporada)
                coleccion_tres = formar_colecciones(base_de_datos_equipos_o_pilotos)
                equipos_o_pilotos = []
                pilotos_o_equipos_por_temporada = schema_dos(coleccion_dos.find({"temporada":temporada_oid}))
                if not pilotos_o_equipos_por_temporada:
                    errores_simples.error_sin_documentos_en_la_base_de_datos("Sin equipos o pilotos" ,base_de_datos_por_temporada)
                for piloto_o_equipo in pilotos_o_equipos_por_temporada:
                    oid = funciones_logicas.validate_object_id(piloto_o_equipo[campo_equipo_o_piloto])
                    temporal = coleccion_tres.find_one({"_id":oid})
                    equipos_o_pilotos.append(temporal)
                
            if not equipos_o_pilotos:
                errores_simples.error_sin_documentos_en_la_base_de_datos("Sin equipos o pilotos" ,base_de_datos_equipos_o_pilotos)
            tabla_posiciones = []
            for equipo_o_piloto in equipos_o_pilotos:

                id = equipo_o_piloto["_id"]
                equipo_o_piloto_id = funciones_logicas.validate_object_id(id)
                team_or_driv = coleccion_tres.find_one({"_id":equipo_o_piloto_id})
                nombre = team_or_driv[campo_equipo_o_piloto]
                carreras_de_un_equipo = schema(
                coleccion.find({
                    campo_carrera: {"$regex": f"^{nombre}$", "$options": "i"},
                    "temporada":temporada_oid
                }))
                cantidad_carreras = coleccion.count_documents({
                    campo_carrera: {"$regex": f"^{nombre}$", "$options": "i"},
                    "temporada":temporada_oid
                })
                
                puntos_totales = sum(carrera[puntos] for carrera in carreras_de_un_equipo)
                
                tabla_posiciones.append({
                    "nombre"              : nombre,
                    "puntos"              : puntos_totales,
                    "cantidad_de_carreras": cantidad_carreras,
                    "temporada"           : temporada["descripcion"],
                    "year"                : year,
                    "categoria"           : categoria
                })

            posiciones = sorted(tabla_posiciones, key=lambda c: (-c["puntos"], -c["cantidad_de_carreras"]))
            for i , posicion in enumerate(posiciones, start=1):
                posicion["posicion"] = i
            return posiciones
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
        
        
def retornar_temporada_oid_por_categoria_y_año(categoria:str, year:int):
    temporada = db_client.Temporadas.find_one({"categoria":categoria, "year":year})
    if not temporada:
        return None
    temporada_id = temporada["_id"]
    temporada_oid = funciones_logicas.validate_object_id(temporada_id)
    return temporada_oid

def buscar_datos_por_temporada(base_de_datos:str):
    if base_de_datos == "Carreras_por_pilotos":
        base_de_datos_dos  = "Pilotos_por_temporada"
        base_de_datos_tres = "Pilotos"
        schema_dos  = pilotos_por_temporada_schema
        schema_tres = pilotos_schema
    elif base_de_datos == "Carreras_por_equipos":
        base_de_datos_dos  = "Equipos_por_temporada"
        base_de_datos_tres = "Equipos"
        schema_dos  = equipos_schema
        schema_tres = equipos_historicos_schema
    else:
        return "false", "false", "false", "false"
    
    return base_de_datos_dos, base_de_datos_tres, schema_dos, schema_tres

def formar_colecciones(base_de_datos:str):
    coleccion = getattr(db_client, base_de_datos)
    return coleccion


def busqueda_campos(base_de_datos:str):
        if base_de_datos == "Carreras_por_pilotos":
            campo_equipo_o_piloto  = "piloto_participante"
            campo_carrera          = "piloto_participante"
            puntos                 = "puntos_piloto"
        else:
            campo_equipo_o_piloto  = "nombre_equipo"
            campo_carrera          = "equipo_participante"
            puntos                 = "puntos_equipo"
            
        return campo_equipo_o_piloto, campo_carrera, puntos