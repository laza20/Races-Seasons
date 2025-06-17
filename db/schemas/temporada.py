def temporada_schema (data)->dict:
        return {
            "_id"                                : str(data["_id"]),
            "descripcion"                        : str(data["descripcion"]).title().strip(),
            "cantidad_de_grandes_premios"        : int(data["cantidad_de_grandes_premios"]),
            "cantidad_de_equipos"                : int(data["cantidad_de_equipos"]),
            "observaciones"                      : str(data["observaciones"]).title().strip(),
            "tipo"                               : str(data["tipo"]),
            "year"                               : int(data["year"]),
            "categoria"                          : str(data["categoria"]),
            "estado"                             : bool(data["estado"]),
            }


def temporadas_schema(datas)->list:
    return [temporada_schema(data) for data in datas]