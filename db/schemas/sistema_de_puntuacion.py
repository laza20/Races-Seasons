def punto_schema(punto)->dict:
        return {
            "id"                      : str(punto["_id"]),
            "posicion"                : int(punto["posicion"]),
            "puntos"                  : int(punto["puntos"]),
            "temporada"               : str(punto["temporada"]),
            "tipo"                    : str(punto["tipo"]),
            "estado"                  : bool(punto["estado"])}
        
def punto_temporada_schema(punto)->dict:
        return {
            "posicion"                : int(punto["posicion"]),
            "puntos"                  : int(punto["puntos"]),
            "temporada"               : str(punto["temporada"]),
            "tipo"                    : str(punto["tipo"]),
            "estado"                  : bool(punto["estado"])}
        
def puntos_schema(puntos)->list:
    return [punto_schema(punto) for punto in puntos]

def puntos_temporada_schema(puntos)->list:
    return [punto_schema(punto) for punto in puntos]