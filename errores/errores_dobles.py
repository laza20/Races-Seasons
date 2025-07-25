from fastapi import HTTPException, status


def error_doble_negativo(base_de_datos, dato_uno, dato_dos):
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=f"No se encontraron datos existentes en '{base_de_datos}' con los datos = '{dato_uno}' y '{dato_dos}'"
        )
        
def error_doble_positivo(base_de_datos, campo_uno, campo_dos, dato_uno, dato_dos):
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=f"Ya existe un documento en '{base_de_datos}' con {campo_uno} = '{dato_uno}' y {campo_dos} = '{dato_dos}'"
        )