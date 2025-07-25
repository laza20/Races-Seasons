listas_de_campos = {
    "Circuitos": ["_id", "ciudad_circuito", "pais_circuito", "distancia_del_circuito", "sistema_medicion", "tipo", "estado"],
    "Conformacion_de_equipos": ["_id", "nombre_equipo", "primer_piloto", "segundo_piloto", "piloto_reserva", "otro_piloto", "otro_piloto_dos", "temporada", "tipo", "estado"],
    "Equipos": ["_id", "nombre_equipo", "pais_equipo", "tipo", "estado"],
    "Circuitos_por_temporada": ["_id", "circuito", "ciudad_circuito", "pais_circuito", "distancia_del_circuito", "temporada", "tipo", "estado"],
    "Equipos_por_temporada": ["_id", "nombre_equipo", "pais_equipo", "equipo_actual", "temporada", "tipo", "estado"],
    "Pilotos_por_temporada": ["_id", "piloto_participante", "edad_piloto", "nacionalidad_piloto", "temporada", "tipo", "estado"],
    "PuntosPorPosicionCarrera": ["_id", "posicion", "puntos", "temporada", "tipo", "tipo_carrera", "estado"],
    "Temporadas": ["_id", "descripcion", "cantidad_de_grandes_premios", "cantidad_de_equipos", "observaciones", "tipo", "year", "categoria", "estado"],
    "Piloto": ["_id", "piloto_participante", "edad_piloto", "nacionalidad_piloto", "tipo", "estado"]
}