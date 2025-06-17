def equipo_schema (equipo)->dict:
        return {
            "id"                 : str(equipo["_id"]),
            "nombre_equipo"      : str(equipo["nombre_equipo"]).title().strip(),
            "pais_equipo"        : str(equipo["pais_equipo"]).title().strip(),
            "tipo"               : str(equipo["tipo"]),
            "estado"             : str(equipo["estado"])}
        
def equipo_carga_schema (equipo)->dict:
        return {
            "nombre_equipo"      : str(equipo["nombre_equipo"]).title().strip(),
            "pais_equipo"        : str(equipo["pais_equipo"]).title().strip(),
            "tipo"               : str(equipo["tipo"]),
            "estado"             : str(equipo["estado"])}
        
def equipo_historico_schema (equipo)->dict:
        return {
            "id"                 : str(equipo["_id"]),
            "nombre_equipo"      : str(equipo["nombre_equipo"]).title().strip(),
            "pais_equipo"        : str(equipo["pais_equipo"]).title().strip(),
            "equipo_actual"      : str(equipo["equipo_actual"]).title().strip(),
            "temporada"          : str(equipo["temporada"]),
            "tipo"               : str(equipo["tipo"]),
            "estado"             : str(equipo["estado"])}

def equipos_schema(equipos)->list:
    return [equipo_schema(equipo) for equipo in equipos]

def equipos_historicos_schema(equipos)->list:
    return [equipo_historico_schema(equipo) for equipo in equipos]

def equipos_carga_schema(equipos)->list:
    return [equipo_carga_schema(equipo) for equipo in equipos]