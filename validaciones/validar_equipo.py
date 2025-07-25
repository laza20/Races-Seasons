from fastapi import HTTPException, status
from validaciones_generales import validaciones_generales_dobles

def validacion_carga_equipo(datos, base_de_datos):
    if isinstance(datos, list) and len(datos) >= 2:
        equipos = set()
        for dato in datos:
            
            key = validacion_carga_equipo_2(dato, base_de_datos)
            
            if key in equipos:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Mismo Equipo ingresado 2 veces")
            equipos.add(key)
    else:
        dato = datos if not isinstance(datos, list) else datos[0]
        key = validacion_carga_equipo_2(dato, base_de_datos)
        
def validacion_carga_equipo_2(dato, base_de_datos):
    key = (dato.nombre_equipo.lower(), dato.pais_equipo.lower())
    validaciones_generales_dobles.validacion_doble_general(base_de_datos, dato.nombre_equipo, dato.pais_equipo)
    return key
        