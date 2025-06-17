def carrera_schema(carrera)->dict:
        return {
            "id"                      : str(carrera["_id"]),
            "piloto_participante"     : str(carrera["piloto_participante"]).title().strip(),
            "equipo_participante"     : str(carrera["equipo_participante"]).title().strip(),
            "posicion"                : int(carrera["posicion"]),
            "ciudad_circuito"         : str(carrera["ciudad_circuito"]).title().strip(),
            "dnf"                     : bool(carrera["dnf"]),
            "temporada"               : str(carrera["temporada"]),
            "tipo"                    : str(carrera["tipo"]),
            "estado"                  : bool(carrera["estado"])}

        
def carreras_schema(carreras)->list:
    return [carrera_schema(carrera) for carrera in carreras]
