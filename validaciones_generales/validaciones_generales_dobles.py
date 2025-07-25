from db.client import db_client
from validaciones_generales.lista_de_campos import listas_de_campos
from errores import errores_dobles, errores_simples

def validacion_doble_general(base_de_datos, dato_uno, dato_dos):
    if base_de_datos not in listas_de_campos:
        errores_simples.error_sin_base_de_datos(base_de_datos)
    coleccion = getattr(db_client, base_de_datos)
    campos = listas_de_campos[base_de_datos]
    
    if isinstance(dato_uno, str) and isinstance(dato_dos, str):
        validacion_doble_str(coleccion,campos, base_de_datos, dato_uno, dato_dos)
    elif isinstance(dato_uno, str) or isinstance(dato_dos, str):
        validacion_doble_one_str(coleccion,campos, base_de_datos, dato_uno, dato_dos)
    else:
        validacion_doble_no_str(coleccion,campos, base_de_datos, dato_uno, dato_dos)
        
        

def validacion_doble_str(coleccion,campos, base_de_datos, dato_uno, dato_dos):
    for i, campo_uno in enumerate(campos):
        for j, campo_dos in enumerate(campos):
            if i == j:
                continue  # Evita comparar el mismo campo contra sí mismo
            
            query = {
                campo_uno: {"$regex": f"^{dato_uno}$", "$options": "i"},
                campo_dos:{"$regex": f"^{dato_dos}$", "$options": "i"}
            }
            
            if coleccion.find_one(query):
                errores_dobles.error_doble_positivo(base_de_datos, campo_uno, campo_dos, dato_uno, dato_dos)
    
def validacion_doble_one_str(coleccion,campos, base_de_datos, dato_uno, dato_dos):
    
    for i, campo_uno in enumerate(campos):
        for j, campo_dos in enumerate(campos):
            if i == j:
                continue  # Evita comparar el mismo campo contra sí mismo
            if isinstance(dato_uno, str):
                query = {
                campo_uno: {"$regex": f"^{dato_uno}$", "$options": "i"},
                campo_dos: dato_dos
                }
            
                if coleccion.find_one(query):
                    errores_dobles.error_doble_positivo(base_de_datos, campo_uno, campo_dos, dato_uno, dato_dos)
            else:
                query = {
                campo_uno: dato_uno,
                campo_dos: {"$regex": f"^{dato_dos}$", "$options": "i"},
                }
                
                if coleccion.find_one(query):
                    errores_dobles.error_doble_positivo(base_de_datos, campo_uno, campo_dos, dato_uno, dato_dos)



def validacion_doble_no_str(coleccion,campos, base_de_datos, dato_uno, dato_dos):
    for i, campo_uno in enumerate(campos):
        for j, campo_dos in enumerate(campos):
            if i == j:
                continue  # Evita comparar el mismo campo contra sí mismo
            
            query = {
                campo_uno : dato_uno,
                campo_dos : dato_dos
            }

            if coleccion.find_one(query):
                errores_dobles.error_doble_positivo(base_de_datos, campo_uno, campo_dos, dato_uno, dato_dos)


def validacion_doble_negativa_general(base_de_datos, dato_uno, dato_dos):
    if base_de_datos not in listas_de_campos:
        errores_simples.error_sin_base_de_datos(base_de_datos)
    coleccion = getattr(db_client, base_de_datos)
    campos = listas_de_campos[base_de_datos]
    
    if isinstance(dato_uno, str) and isinstance(dato_dos, str):
        validacion_doble_negativa_str(coleccion,campos, base_de_datos, dato_uno, dato_dos)
    elif isinstance(dato_uno, str) or isinstance(dato_dos, str):
        validacion_doble_negativa_one_str(coleccion,campos, base_de_datos, dato_uno, dato_dos)
    else:
        validacion_doble_negativa_no_str(coleccion,campos, base_de_datos, dato_uno, dato_dos)
        
        
def validacion_doble_negativa_str(coleccion,campos, base_de_datos, dato_uno, dato_dos):
    for i, campo_uno in enumerate(campos):
        for j, campo_dos in enumerate(campos):
            if i == j:
                continue  # Evita comparar el mismo campo contra sí mismo
            
            query = {
                campo_uno: {"$regex": f"^{dato_uno}$", "$options": "i"},
                campo_dos:{"$regex": f"^{dato_dos}$", "$options": "i"}
            }
            
            if coleccion.find_one(query):
                return
                
    errores_dobles.error_doble_negativo(base_de_datos, dato_uno, dato_dos)
    
    

def validacion_doble_negativa_one_str(coleccion,campos, base_de_datos, dato_uno, dato_dos):
    for i, campo_uno in enumerate(campos):
        for j, campo_dos in enumerate(campos):
            if i == j:
                continue  # Evita comparar el mismo campo contra sí mismo
            if isinstance(dato_uno, str):
                query = {
                campo_uno: {"$regex": f"^{dato_uno}$", "$options": "i"},
                campo_dos: dato_dos
                }
            
                if coleccion.find_one(query):
                    return
            else:
                query = {
                campo_uno: dato_uno,
                campo_dos: {"$regex": f"^{dato_dos}$", "$options": "i"},
                }
                
                if coleccion.find_one(query):
                    return
                    
                    
    errores_dobles.error_doble_negativo(base_de_datos, dato_uno, dato_dos)







def validacion_doble_negativa_no_str(coleccion,campos, base_de_datos, dato_uno, dato_dos):
    for i, campo_uno in enumerate(campos):
        for j, campo_dos in enumerate(campos):
            if i == j:
                continue  # Evita comparar el mismo campo contra sí mismo
            
            query = {
                campo_uno : dato_uno,
                campo_dos : dato_dos
            }

            if coleccion.find_one(query):
                return
            
    errores_dobles.error_doble_negativo(base_de_datos, dato_uno, dato_dos)