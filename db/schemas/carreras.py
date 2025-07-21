def carrera_schema(carrera)->dict:
        return {
            "id"                      : str(carrera["_id"]),
            "piloto_participante"     : str(carrera["piloto_participante"]).title().strip(),
            "equipo_participante"     : str(carrera["equipo_participante"]).title().strip(),
            "posicion"                : int(carrera["posicion"]),
            "vuelta_rapida_piloto"    : str(carrera["vuelta_rapida_piloto"]),
            "vuelta_rapida_equipo"    : str(carrera["vuelta_rapida_equipo"]),
            "ciudad_circuito"         : str(carrera["ciudad_circuito"]).title().strip(),
            "dnf"                     : bool(carrera["dnf"]),
            "fecha"                   : str(carrera["fecha"]),
            "temporada"               : str(carrera["temporada"]),
            "tipo"                    : str(carrera["tipo"]),
            "estado"                  : bool(carrera["estado"])}
        
def carrera_carga_schema(carrera)->dict:
    return {
        "piloto_participante"     : str(carrera["piloto_participante"]).title().strip(),
        "equipo_participante"     : str(carrera["equipo_participante"]).title().strip(),
        "posicion"                : int(carrera["posicion"]),
        "vuelta_rapida_piloto"    : str(carrera["vuelta_rapida_piloto"]),
        "vuelta_rapida_equipo"    : str(carrera["vuelta_rapida_equipo"]),
        "ciudad_circuito"         : str(carrera["ciudad_circuito"]).title().strip(),
        "dnf"                     : bool(carrera["dnf"]),
        "fecha"                   : str(carrera["vuelta_rapida_equipo"]),
        "temporada"               : str(carrera["temporada"]),
        "tipo"                    : str(carrera["tipo"]),
        "estado"                  : bool(carrera["estado"])}

        
def carreras_schema(carreras)->list:
    return [carrera_schema(carrera) for carrera in carreras]

def carreras_carga_schema(carreras)->list:
    return [carrera_carga_schema(carrera) for carrera in carreras]
