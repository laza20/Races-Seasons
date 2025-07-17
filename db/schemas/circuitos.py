def circuito_schema (circuito)->dict:
        return {
            "id"                      : str(circuito["_id"]),
            "ciudad_circuito"         : str(circuito["ciudad_circuito"]).title().strip(),
            "pais_circuito"           : str(circuito["pais_circuito"]).capitalize().strip(),
            "distancia_del_circuito"  : float(circuito["distancia_del_circuito"]),
            "sistema_medicion"        : str(circuito["sistema_medicion"]).upper().strip(),
            "tipo"                    : str(circuito["tipo"]),
            "estado"                  : bool(circuito["estado"])
            }
        
def circuito_carga_schema (circuito)->dict:
        return {
            "ciudad_circuito"         : str(circuito["ciudad_circuito"]).title().strip(),
            "pais_circuito"           : str(circuito["pais_circuito"]).capitalize().strip(),
            "distancia_del_circuito"  : float(circuito["distancia_del_circuito"]),
            "sistema_medicion"        : str(circuito["sistema_medicion"]).upper().strip(),
            "tipo"                    : str(circuito["tipo"]),
            "estado"                  : bool(circuito["estado"])
            }
        
def circuito_carga_por_temporada_schema (circuito)->dict:
        return {
            "circuito"                : str(circuito["circuito"]),
            "temporada"               : str(circuito["temporada"]),
            "estado"                  : bool(circuito["estado"])
            }
        
def circuito_por_temporada_schema (circuito)->dict:
        return {
            "id"                      : str(circuito["_id"]),
            "circuito"                : str(circuito["circuito"]),
            "ciudad_circuito"         : str(circuito["ciudad_circuito"]).title().strip(),
            "pais_circuito"           : str(circuito["pais_circuito"]).capitalize().strip(),
            "distancia_del_circuito"  : float(circuito["distancia_del_circuito"]),
            "temporada"               : str(circuito["temporada"]),
            "tipo"                    : str(circuito["tipo"]),
            "estado"                  : bool(circuito["estado"])
            }
        
def circuitos_schema(circuitos)->list:
    return [circuito_schema(circuito) for circuito in circuitos]

def circuitos_carga_schema(circuitos)->list:
    return [circuito_carga_schema(circuito) for circuito in circuitos]

def circuitos_por_temporada_schema(circuitos)->dict:
    return [circuito_por_temporada_schema(circuito) for circuito in circuitos]

def circuitos_por_temporada_carga_schema(circuitos) ->list:
    return [circuito_carga_por_temporada_schema(circuito) for circuito in circuitos]
    
