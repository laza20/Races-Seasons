from fastapi import HTTPException, status
from validaciones_generales import validaciones_generales_dobles


def validacion_carga_piloto(datos, base_de_datos):
    if isinstance(datos, list) and len(datos) >= 2:
        pilotos = set()
        for dato in datos:
            key = validacion_carga_piloto_2(dato, base_de_datos)
            validar_carga_repetida(key, pilotos, dato)
            pilotos.add(key)   
    else:
        dato = datos if not isinstance(datos, list) else datos[0]
        key = validacion_carga_piloto_2(dato, base_de_datos)
            
def validar_carga_repetida(key, pilotos, dato):
    if key in pilotos:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Mismo piloto ingresado 2 veces {dato.piloto_participante}")
            
def validacion_carga_piloto_2(dato, base_de_datos):
    key = create_key(dato) 
    validaciones_generales_dobles.validacion_doble_general(base_de_datos, dato.piloto_participante, dato.edad_piloto)
    return key

def create_key(dato):
    key = (dato.piloto_participante.lower(), dato.edad_piloto)   
    return key