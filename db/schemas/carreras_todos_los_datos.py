def carrera_todos_los_datos_schema_una_carrera(carrera, piloto, equipo) -> tuple[dict, dict, dict]:
    datos_carrera = {
        "id": str(carrera["_id"]),
        "piloto_participante": str(carrera["piloto_participante"]).title().strip(),
        "equipo_participante": str(carrera["equipo_participante"]).title().strip(),
        "posicion"           : int(carrera["posicion"]),
        "ciudad_circuito"    : str(carrera["ciudad_circuito"]).title().strip(),
        "dnf"                :bool(carrera["dnf"]),
        "fecha"              : str(equipo["fecha"]),
        "temporada"          : str(carrera["temporada"]),
        "tipo_carrera"               : str(carrera["tipo_carrera"]),
        "tipo"               : str(carrera["tipo"]),
        "estado"             : bool(carrera["estado"]),
    }

    datos_carrera_equipo = {
        "id": str(equipo["_id"]),
        "equipo_participante": str(equipo["equipo_participante"]).title().strip(),
        "puntos_equipo"      : int(equipo["puntos_equipo"]),
        "ciudad_circuito"    : str(equipo["ciudad_circuito"]).title().strip(),
        "cant_dnf"           : int(equipo["cant_dnf"]),
        "fecha"              : str(equipo["fecha"]),
        "temporada"          : str(equipo["temporada"]),
        "tipo_carrera"               : str(carrera["tipo_carrera"]),
        "tipo"               : str(equipo["tipo"]),
        "estado"             : bool(equipo["estado"]),
    }
    
    datos_carrera_piloto = {
        "id": str(piloto["_id"]),
        "piloto_participante": str(piloto["piloto_participante"]).title().strip(),
        "puntos_piloto"      : int(piloto["puntos_piloto"]),
        "ciudad_circuito"    : str(piloto["ciudad_circuito"]).title().strip(),
        "dnf"                : bool(piloto["dnf"]),
        "fecha"              : str(equipo["fecha"]),
        "temporada"          : str(equipo["temporada"]),
        "tipo_carrera"               : str(carrera["tipo_carrera"]),
        "tipo"               : str(piloto["tipo"]),
        "estado"             : bool(piloto["estado"]),
    }
    
    
    return datos_carrera, datos_carrera_equipo, datos_carrera_piloto
        
def carrera_todos_los_datos_schema_todas_las_carrera(datas) -> list:
    return [carrera_todos_los_datos_schema_una_carrera(carrera, piloto, equipo)[0] for carrera, piloto, equipo in datas]
