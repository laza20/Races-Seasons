from fastapi import HTTPException, status
from validaciones_generales import validaciones_generales_dobles
        

        
def validar_carga_circuito(datos, base_de_datos):
    # Si es una lista con más de un circuito
    if isinstance(datos, list) and len(datos) >= 2:
        ciudades = set()
        for dato in datos:
            key = validar_carga_circuito_2(dato, base_de_datos)
            if key in ciudades:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Mismo circuito ingresado 2 veces")
            ciudades.add(key)
    else:
        # Es un único circuito
        dato = datos if not isinstance(datos, list) else datos[0]
        key = validar_carga_circuito_2(dato, base_de_datos)

        
        
def validar_carga_circuito_2(dato, base_de_datos):
    key = (dato.pais_circuito.lower(), dato.ciudad_circuito.lower())
    
    validaciones_generales_dobles.validacion_doble_general(base_de_datos, dato.pais_circuito,dato.ciudad_circuito )

    return key