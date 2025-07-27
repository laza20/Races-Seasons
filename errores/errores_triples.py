from fastapi import HTTPException, status


def error_triple_negativo(base_de_datos, dato_uno, dato_dos, dato_tres):
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=f"No se encontraron datos existentes en '{base_de_datos}' con los datos = '{dato_uno}', '{dato_dos}' y '{dato_tres}'"
        )
        
def error_triple_positivo(base_de_datos, campo_uno, campo_dos,campo_tres, dato_uno, dato_dos, dato_tres):
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=f"Ya existe un documento en '{base_de_datos}' con {campo_uno} = '{dato_uno}', {campo_dos} = '{dato_dos}' y {campo_tres} = '{dato_tres}'"
        )



