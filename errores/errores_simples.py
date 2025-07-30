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

def error_sin_base_de_datos(base_de_datos):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No hay definición de campos para la colección {base_de_datos}"
        )


def error_sin_oid(dato, base_de_datos):
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT, 
        detail=f"El dato {dato} no fue encontrado en la base de datos {base_de_datos} con ningun documentos, por ende no podemos retornar un ID del mismo.")
    
    
def error_sin_documentos_en_la_base_de_datos(dato, base_de_datos):
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT, 
        detail=f"El dato {dato} no fue encontrado en la base de datos {base_de_datos} con ningun documentos, por ende no podemos dar retorno por sobre el mismo.")
    