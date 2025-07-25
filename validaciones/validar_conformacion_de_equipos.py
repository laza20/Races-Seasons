from db.client import db_client
from fastapi import HTTPException, status
from funciones import funciones_logicas
from validaciones_generales import validaciones_generales_dobles, validaciones_generales_simples


#VALIDAR QUE EL PRIMERO Y EL SEGUNDO PILOTO SEAN DIFERENTES
def validar_carga_de_conformacion_de_equipos(datos, base_de_datos):
    
        # Si es una lista con más de un circuito
    if isinstance(datos, list) and len(datos) >= 2:
        equipos = set()
        for dato in datos:
            key = validar_carga_de_conformacion_de_equipos_2(dato, datos, base_de_datos)
            # Verificar duplicados en la misma carga
            if key in equipos:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Conformacion de equipo duplicada en la entrega"
                )
            equipos.add(key)

    else:
        # Es un único circuito
        dato = datos if not isinstance(datos, list) else datos[0]
        validar_carga_de_conformacion_de_equipos_2(dato,  datos, base_de_datos)
                


#Funcion para evitar la duplicidad de la carga de documentos de circuitos por temporada
def validar_carga_de_conformacion_de_equipos_2(dato,  datos, base_de_datos):
        temporada_oid = funciones_logicas.validate_object_id(dato.temporada)
        conformacion_oid = funciones_logicas.validate_object_id_or_false(dato.id)
        
        key = (temporada_oid, conformacion_oid)
        
        buscar_pilotos = verificar_pilotos(dato)
        validar_busqueda_de_pilotos(buscar_pilotos, temporada_oid)
        
        
        
        validaciones_generales_simples.validacion_simple_general_negativa("Equipos", dato.nombre_equipo)
        equipo = db_client.Equipos.find_one({"nombre_equipo": {"$regex": f"^{dato.nombre_equipo}$", "$options": "i"}})
        equipo_oid = equipo["_id"]


        validaciones_generales_dobles.validacion_doble_general(base_de_datos, temporada_oid, dato.nombre_equipo)
        
        validaciones_generales_dobles.validacion_doble_negativa_general("Equipos_por_temporada", equipo_oid, temporada_oid)
        
            
        return key
    

def verificar_pilotos(dato):
        buscar_pilotos = {}
        if dato.primer_piloto and dato.segundo_piloto: 
            buscar_pilotos["primer_piloto"] = dato.primer_piloto.strip()
            buscar_pilotos["segundo_piloto"] = dato.segundo_piloto.strip()
        else:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                    detail="El primer y segundo piloto deben estar cargados")
        if dato.piloto_reserva:
            buscar_pilotos["piloto_reserva"] = dato.piloto_reserva.strip()
        if dato.otro_piloto:
            buscar_pilotos["otro_piloto"] = dato.otro_piloto.strip()
        if dato.otro_piloto_dos:
            buscar_pilotos["otro_piloto_dos"] = dato.otro_piloto_dos.strip()
            
        return buscar_pilotos
    
def validar_busqueda_de_pilotos(buscar_pilotos, temporada_oid):
        #clave se utiliza para separa el nombre del piloto y su posicion en el equipo pasa de sin clave'('primer_piloto', 'Pierre Gasly') a con clave Pierre Gasly'
        for  clave, nombre in buscar_pilotos.items():
            if not nombre:
                nombre = "Null"
                continue
            validaciones_generales_simples.validacion_simple_general_negativa("Pilotos", nombre )
            piloto = db_client.Pilotos.find_one({"piloto_participante": nombre})
            validaciones_generales_simples.validacion_simple_general_negativa("Pilotos", piloto["_id"])
            validaciones_generales_dobles.validacion_doble_negativa_general("Pilotos_por_temporada", piloto["_id"], temporada_oid)
