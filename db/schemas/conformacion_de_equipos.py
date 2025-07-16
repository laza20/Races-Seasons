def piloto_x_equipo_schema (data)->dict:
        return {
            "id"                       : str(data["_id"]),
            "nombre_equipo"            : str(data["nombre_equipo"]).title().strip(),
            "primer_piloto"            : str(data["primer_piloto"]).title().strip(),
            "segundo_piloto"           : str(data["segundo_piloto"]).title().strip(),
            "piloto_reserva"           : str(data["piloto_reserva"]).title().strip(),
            "otro_piloto"              : str(data["otro_piloto"]).title().strip(),
            "otro_piloto_dos"          : str(data["otro_piloto_dos"]).title().strip(),
            "temporada"                : str(data["temporada"]),
            "tipo"                     : str(data["tipo"]),
            "estado"                   : str(data["estado"])}
        
def piloto_x_equipo_carga_schema (data)->dict:
        return {
            "nombre_equipo"            : str(data["nombre_equipo"]).title().strip(),
            "primer_piloto"            : str(data["primer_piloto"]).title().strip(),
            "segundo_piloto"           : str(data["segundo_piloto"]).title().strip(),
            "piloto_reserva"           : str(data["piloto_reserva"]).title().strip(),
            "otro_piloto"              : str(data["otro_piloto"]).title().strip(),
            "otro_piloto_dos"          : str(data["otro_piloto_dos"]).title().strip(),
            "temporada"                : str(data["temporada"]),
            "tipo"                     : str(data["tipo"]),
            "estado"                   : str(data["estado"])}
        
        
def pilotos_x_equipos_schema(datas)->list:
    return [piloto_x_equipo_schema(data) for data in datas]


def pilotos_x_equipos_cargas_schema(datas)->list:
    return [piloto_x_equipo_carga_schema(data) for data in datas]