def puntos_por_piloto_schema(punto)->dict:
        return {
            "id"                      : str(punto["_id"]),
            "piloto_participante"     : str(punto["piloto_participante"]).title().strip(),
            "puntos_piloto"           : int(punto["puntos_piloto"]),
            "ciudad_circuito"         : str(punto["ciudad_circuito"]).title().strip(),
            "dnf"                     : bool(punto["dnf"]),
            "fecha"                   : str(punto["fecha"]),
            "temporada"               : str(punto["temporada"]),
            "tipo_carrera"            : str(punto["tipo_carrera"]),
            "tipo"                    : str(punto["tipo"]),
            "estado"                  : bool(punto["estado"])}
        

        
def puntos_por_pilotos_schema(puntos)->list:
    return [puntos_por_piloto_schema(punto) for punto in puntos]


