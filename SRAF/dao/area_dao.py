from config.base_datos import obtener_conexion
from config.logger import logger
from config.sistema_config import (AreaDuplicidadError, AreaNoEncontradaError)
from modelos.area import Area

class AreaDao:
    
    def __init__(self):
        self.logger = logger()
        
    def insertar(sefl, area):
        conn = obtener_conexion()
        cursor = conn.cursor()
        #ejecuta la consulta sql y valida si ahi duplicidad
        cursor.execute("""
            SELECT nombre
            FROM area
            WHERE nombre = ?            
            """, area.nombre)
        if cursor.fetchone():
            conn.close()
            
            raise AreaDuplicidadError(
                area.nombre
            )