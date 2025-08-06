#pyright: reportInvalidTypeForm=false
from funciones import funciones_logicas
from fastapi import status
from db.client import db_client
from funciones import funciones_logicas
from fastapi import  HTTPException, status
from errores import errores_simples
from db.models.carrera_todos_los_datos import DatosTotales
from db.schemas.carreras_todos_los_datos import  carrera_todos_los_datos_schema_una_carrera
from db.schemas.sistema_de_puntuacion import puntos_schema
from db.schemas.temporada import temporadas_schema
from funciones import funciones_busqueda
from funciones import funciones_podios

def view_old_data_of_season(router):
    @router.get("/Totales/{temporada}",  response_model=DatosTotales)
    async def obtener_datos_totales(temporada:str):
        temporada_oid = funciones_logicas.validate_object_id(temporada)
        todas_las_carreras_de_una_temporada = funciones_busqueda.encontrar_muchos_documentos(temporada_oid, "Carreras")
        todas_las_carreras_de_un_piloto_temporada = funciones_busqueda.encontrar_muchos_documentos(temporada_oid, "Carreras_por_pilotos")
        todas_las_carreras_de_un_equipo_temporada = funciones_busqueda.encontrar_muchos_documentos(temporada_oid, "Carreras_por_equipos")

        
        lista_carrera, lista_puntos_equipo, lista_puntos_piloto = [], [], []
        
        for carrera, piloto, equipo in zip(todas_las_carreras_de_una_temporada, todas_las_carreras_de_un_piloto_temporada,todas_las_carreras_de_un_equipo_temporada):
            datos_carrera, datos_equipo, datos_piloto = carrera_todos_los_datos_schema_una_carrera(carrera, piloto, equipo)
            lista_carrera.append(datos_carrera)
            lista_puntos_equipo.append(datos_equipo)
            lista_puntos_piloto.append(datos_piloto)
            
        return  DatosTotales(
            carreras=lista_carrera,
            puntos_x_equipo=lista_puntos_equipo,
            puntos_x_piloto=lista_puntos_piloto
    )
        
#Sirve para carreras, carreras_por_piloto, carreras_por_equipos
def view_data_season_and_city(router, base_de_datos, schema):
    @router.get("/Ciudad/{temporada}/{ciudad_circuito}")
    async def show_carreras_city(ciudad_circuito: str, temporada:str):
        coleccion = getattr(db_client, base_de_datos)
        temporada_oid = funciones_logicas.validate_object_id(temporada)
        carreras = schema(coleccion.find({"ciudad_circuito":ciudad_circuito, "temporada": temporada_oid}))
        if not carreras:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontraron carreras")
        
        return carreras
    
def  view_data_for_category_and_year(router, base_de_datos, schema):
    @router.get("/Data/Por/{categoria}/{year}")
    async def view_data_for_category_and_year(categoria:str, year:int ):
        coleccion = getattr(db_client, base_de_datos)
        season = db_client.Temporadas.find_one({"categoria":categoria, "year":year})
        if not season:
            errores_simples.error_simple_negativo(f"{categoria}-{year}", base_de_datos)
        temporada_oid = funciones_logicas.validate_object_id(season["_id"])
        documentos = schema(coleccion.find({"temporada":temporada_oid}))
        return documentos
        
#puntos_por_pilotos_schema--campo sirve para verificar por que campo se va a ordenar (puntos_piloto, puntos_equipo, puntos)
def  view_data_for_season_city_and_type_race(router, base_de_datos, schema, campo):
    @router.get("/Circuito/{temporada}/{ciudad_circuito}/{tipo_carrera}")
    async def show_carrera_by_city_and_year(ciudad_circuito: str, temporada:str, tipo_carrera:str):
        coleccion = getattr(db_client, base_de_datos)
        temporada_oid = funciones_logicas.validate_object_id(temporada)
        pilotos = schema(coleccion.find({"ciudad_circuito":ciudad_circuito, 
                                         "temporada":temporada_oid, 
                                         "tipo_carrera":tipo_carrera}))
    
        posicion = sorted(pilotos, key=lambda c: c[campo], reverse=True) #ordena el dict por puntos.
        return posicion





#schema = puntos_por_pilotos_schema
def view_podiums_season_by_id_season(router, base_de_datos, schema):
    @router.get("/Podios/Temporada/{dato}/{temporada}")
    async def show_podiums_season(dato:str, temporada:str):
        coleccion = getattr(db_client, base_de_datos)
        temporada_oid = funciones_logicas.validate_object_id(temporada)
        dict_dato, campo  =  funciones_podios.buscar_data_team_or_driver(base_de_datos, dato, temporada_oid)
        carreras_totales = schema(coleccion.find({
            campo : {"$regex": f"^{dato}$", "$options": "i"},
            "temporada":temporada_oid
        }))
        puntos_por_posicion = puntos_schema(db_client.Sistema_de_puntuacion.find({"temporada":temporada_oid}))
        primer_lugar, segundo_lugar, tercer_lugar, podios =  funciones_podios.buscar_podios(carreras_totales, puntos_por_posicion, base_de_datos)
        podios =  funciones_podios.transformacion_temporada(base_de_datos, podios, dict_dato, primer_lugar, segundo_lugar, tercer_lugar, dato, temporada_oid)
        return podios

def view_podiums_season_by_category_and_year(router, base_de_datos, schema):
    @router.get("/Podios/Año/{year}/Categoria/{categoria}/Dato/{dato}", )
    async def show_podiums_for_drivers(dato:str, year:int, categoria:str):
        coleccion = getattr(db_client, base_de_datos)
        season = db_client.Temporadas.find_one({"year":year, "categoria":categoria})
        if not season:
            errores_simples.error_sin_documentos_en_la_base_de_datos(f"{categoria}-{year}", "Temporadas")
            
        temporada_oid = funciones_logicas.validate_object_id(season["_id"])
        
        dict_dato, campo = funciones_podios.buscar_data_team_or_driver(base_de_datos, dato, temporada_oid)
        
        carreras_totales = schema(coleccion.find({
            campo : {"$regex": f"^{dato}$", "$options": "i"},
            "temporada":temporada_oid
        }))
        
        puntos_por_posicion = puntos_schema(db_client.Sistema_de_puntuacion.find({"temporada":temporada_oid}))
                
        primer_lugar, segundo_lugar, tercer_lugar, podios =  funciones_podios.buscar_podios(carreras_totales, puntos_por_posicion, base_de_datos)

        podios =  funciones_podios.transformacion_temporada(base_de_datos, podios, dict_dato, primer_lugar, segundo_lugar, tercer_lugar, dato, temporada_oid)
        return podios

    
def view_olds_podiums_for_driver_or_teams_by_category(router, base_de_datos, schema):
    @router.get("/Podios/Totales/Dato/{dato}/Categoria/{categoria}")
    async def show_podiums_for_drivers(dato:str, categoria:str):
        coleccion = getattr(db_client, base_de_datos)
        temporadas = temporadas_schema(db_client.Temporadas.find({"categoria":{"$regex": f"^{categoria}$", "$options": "i"}}))
        if not temporadas:
            errores_simples.error_sin_documentos_en_la_base_de_datos(categoria, "Temporadas")
            
        #el piloto_participante y nombre_equipo en pilotos_por_temporada y equipos_por_temporada
        #son ids por eso esta funcion se encarga de buscar esos ids y retornarlos como nombres para poder usarlos
        #en la verificacion. lo hace por medio del nombre (tanto del equipo como del piloto)
        dato_oid = funciones_podios.buscar_id_piloto_o_equipo(base_de_datos, dato)
        
        podiums_totales, podiums_primero, podiums_segundo, podiums_tercero = funciones_podios.inicializar_podios_totales()
        for temporada in temporadas:
            temporada_oid = funciones_logicas.validate_object_id(temporada["_id"])
                
            #verifica si el dato esta en la temporada actual del ciclo del bucle
            verificacion = funciones_podios.verificar_existencia_dato_en_temporada(base_de_datos, dato_oid, temporada_oid)
            if verificacion == "false":
                continue
                
            dict_dato, campo =  funciones_podios.buscar_data_team_or_driver(base_de_datos, dato, temporada_oid)
            
            carreras_totales = list(coleccion.find({
                campo : {"$regex": f"^{dato}$", "$options": "i"},
                "temporada":temporada_oid
            }))
        
            puntos_por_posicion = puntos_schema(db_client.Sistema_de_puntuacion.find({"temporada":temporada_oid}))
        
            primer_lugar, segundo_lugar, tercer_lugar, podios =  funciones_podios.buscar_podios(carreras_totales, puntos_por_posicion, base_de_datos)
            print (primer_lugar, segundo_lugar, tercer_lugar)
            podiums_primero += primer_lugar
            podiums_segundo += segundo_lugar
            podiums_tercero += tercer_lugar
            
        podiums_totales = podiums_primero + podiums_segundo + podiums_tercero
        
        
        podios =  funciones_podios.transformacion_total(base_de_datos, podiums_totales, podiums_primero, podiums_segundo, podiums_tercero, dato, categoria)

        
        return podios
    

