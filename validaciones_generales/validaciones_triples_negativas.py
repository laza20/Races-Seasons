from db.client import db_client
from validaciones_generales.lista_de_campos import listas_de_campos
from errores import errores_triples, errores_simples
from itertools import permutations

def validacion_triple_general_negativa(base_de_datos, dato_uno, dato_dos, dato_tres):
    if base_de_datos not in listas_de_campos:
        errores_simples.error_sin_base_de_datos(base_de_datos)
    coleccion = getattr(db_client, base_de_datos)
    campos = listas_de_campos[base_de_datos]
    
    if isinstance(dato_uno, str) and isinstance(dato_dos, str) and isinstance(dato_tres, str):
        validacion_triple_tree_str_negativa(coleccion,campos, base_de_datos, dato_uno, dato_dos, dato_tres)
    elif isinstance(dato_uno, str) and isinstance(dato_dos, str) or isinstance(dato_uno, str) and isinstance(dato_tres, str) or isinstance(dato_dos,str) and isinstance(dato_tres, str):
        validacion_triple_two_str_negativa(coleccion,campos, base_de_datos, dato_uno, dato_dos, dato_tres)
    elif isinstance(dato_tres, str) or isinstance(dato_dos, str) or isinstance(dato_uno, str):
        validacion_triple_one_str(coleccion,campos, base_de_datos, dato_uno, dato_dos, dato_tres)
    else:
        validacion_triple_no_str(coleccion,campos, base_de_datos, dato_uno, dato_dos, dato_tres)
        

def validacion_triple_tree_str_negativa(coleccion,campos, base_de_datos, dato_uno, dato_dos, dato_tres):
    for  campo_uno, campo_dos, campo_tres in permutations(campos, 3):
                query = {
                    campo_uno: {"$regex": f"^{dato_uno}$", "$options": "i"},
                    campo_dos:{"$regex": f"^{dato_dos}$", "$options": "i"},
                    campo_tres:{"$regex": f"^{dato_tres}$", "$options": "i"}
                }
                
                if coleccion.find_one(query):
                    return
                
    errores_triples.error_triple_negativo(base_de_datos, dato_uno, dato_dos, dato_tres)

    
def validacion_triple_two_str_negativa(coleccion,campos, base_de_datos, dato_uno, dato_dos, dato_tres):
    combinaciones_datos = [
        (dato_uno, dato_dos, dato_tres),
        (dato_uno, dato_tres, dato_dos),
        (dato_dos, dato_tres, dato_uno)
    ]
    for  campo_uno, campo_dos, campo_tres in permutations(campos, 3):
        for valor_1, valor_2, valor_3 in combinaciones_datos:
            
            if isinstance(valor_1, str) and isinstance(valor_2, str):
                query = verificacion_doble_str_query(campo_uno, campo_dos, campo_tres, valor_1, valor_2, valor_3)
            
                if coleccion.find_one(query):
                    return
                    
    errores_triples.error_triple_negativo(base_de_datos, dato_uno, dato_dos, dato_tres)

def verificacion_doble_str_query(campo_uno, campo_dos, campo_tres, dato_uno, dato_dos, dato_tres):
            query = {
                campo_uno: {"$regex": f"^{dato_uno}$", "$options": "i"},
                campo_dos: {"$regex": f"^{dato_dos}$", "$options": "i"},
                campo_tres : dato_tres
                }
            
            return query

def validacion_triple_one_str(coleccion,campos, base_de_datos, dato_uno, dato_dos, dato_tres):
    combinaciones = [
        (dato_uno, dato_dos, dato_tres),
        (dato_dos, dato_uno, dato_tres),
        (dato_tres, dato_uno, dato_dos)
    ]

    for campo_uno, campo_dos, campo_tres in permutations(campos, 3):
        for valor_1, valor_2, valor_3 in combinaciones:
            if isinstance(valor_1, str) and not isinstance(valor_2, str) and not isinstance(valor_3, str):
                query = verificacion_one_str_query(campo_uno, campo_dos, campo_tres, valor_1, valor_2, valor_3)
                if coleccion.find_one(query):
                    return
                    
    errores_triples.error_triple_negativo(base_de_datos, dato_uno, dato_dos, dato_tres)

def verificacion_one_str_query(campo_uno, campo_dos, campo_tres, dato_uno, dato_dos, dato_tres):
            query = {
                campo_uno  : {"$regex": f"^{dato_uno}$", "$options": "i"},
                campo_dos  : dato_dos,
                campo_tres : dato_tres
                }
            
            return query
        
def validacion_triple_no_str(coleccion,campos, base_de_datos, dato_uno, dato_dos, dato_tres):
        for campo_uno, campo_dos, campo_tres in permutations(campos, 3):
            query = {
                campo_uno  : dato_uno,
                campo_dos  : dato_dos,
                campo_tres : dato_tres
                }
            
            if coleccion.find_one(query):
                return
        
        errores_triples.error_triple_negativo(base_de_datos, dato_uno, dato_dos, dato_tres)
