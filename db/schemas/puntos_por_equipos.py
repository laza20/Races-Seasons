def puntos_por_equipo_schema(punto)->dict:
        return {
            "id"                      : str(punto["_id"]),
            "equipo_participante"     : str(punto["equipo_participante"]).title().strip(),
            "puntos_equipo"           : int(punto["puntos_equipo"]),
            "ciudad_circuito"         : str(punto["ciudad_circuito"]).title().strip(),
            "cant_dnf"                : int(punto["cant_dnf"]),
            "fecha"                   : str(punto["fecha"]),
            "temporada"               : str(punto["temporada"]),
            "tipo_carrera"            : str(punto["tipo_carrera"]),
            "tipo"                    : str(punto["tipo"]),
            "estado"                  : bool(punto["estado"])}
        

def puntos_por_equipos_schema(puntos)->list:
    return [puntos_por_equipo_schema(punto) for punto in puntos]


