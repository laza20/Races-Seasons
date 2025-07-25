from fastapi import HTTPException, status


def error_simple_negativo(dato, base_de_datos):
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=f"El dato '{dato}' no se encuentra en la base de datos '{base_de_datos}'"
        )
        
def error_simple_positivo(dato, base_de_datos, campo):
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=f"El dato '{dato}' ya se encuentra en la base de datos '{base_de_datos}' en el campo '{campo}'"
        )