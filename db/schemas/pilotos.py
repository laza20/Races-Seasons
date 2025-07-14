def piloto_schema (piloto)->dict:
        return {
            "id"                 : str(piloto["_id"]),
            "piloto_participante": str(piloto["piloto_participante"]).title().strip(),
            "edad_piloto"        : int(piloto["edad_piloto"]),
            "nacionalidad_piloto": str(piloto["nacionalidad_piloto"]).capitalize().strip(),
            "tipo"               : str(piloto["tipo"]).strip(),
            "estado"             : str(piloto["estado"])}
        
def piloto_carga_schema (piloto)->dict:
        return {
            "piloto_participante": str(piloto["piloto_participante"]).title().strip(),
            "edad_piloto"        : int(piloto["edad_piloto"]),
            "nacionalidad_piloto": str(piloto["nacionalidad_piloto"]).capitalize().strip(),
            "estado"             : str(piloto["estado"])}
    
def piloto_por_temporada_schema (piloto)->dict:
        return {
            "id"                 : str(piloto["_id"]),
            "piloto_participante": str(piloto["piloto_participante"]),
            "edad_piloto"        : int(piloto["edad_piloto"]),
            "nacionalidad_piloto": str(piloto["nacionalidad_piloto"]).capitalize().strip(),
            "temporada"          : str(piloto["temporada"]),
            "tipo"               : str(piloto["tipo"]),
            "estado"             : str(piloto["estado"])}


def piloto_por_temporada_carga_schema (piloto)->dict:
        return {
            "piloto_participante": str(piloto["piloto_participante"]).title().strip(),
            "temporada"          : str(piloto["temporada"]).capitalize().strip(),
            "estado"             : str(piloto["estado"])}

def pilotos_schema(pilotos)->list:
    return [piloto_schema(piloto) for piloto in pilotos]

def pilotos_carga_schema(pilotos)->list:
    return [piloto_carga_schema(piloto) for piloto in pilotos]
        
        
def pilotos_por_temporada_schema(pilotos)->list:
    return [piloto_por_temporada_schema(piloto) for piloto in pilotos]

def pilotos_por_temporada_carga_schema(pilotos)->list:
    return [piloto_por_temporada_schema(piloto) for piloto in pilotos]
