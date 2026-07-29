from config.base_datos import obtener_conexion
from config.logger import logger
from config.sistema_config import (AreaDuplicidadError, AreaNoEncontradaError)
from modelos.area import Area

class AreaDao:
    
    def __init__(self):
        self.logger = logger()
        
    def insertar(self, area):
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
        #aqui inserta la nueva area
        cursor.execute("""
            INSERT INTO area
            (
                nombre,
                descripcion
            )
            VALUES
            (
                ?,?
            )
            """,
            area.mombre,
            area.descripcion
            )
        
        conn.commit()
        
        cursor.execute("SELECT @@IDENTITY")
        
        area.id_area = cursor.fetchone()[0]
        
        conn.close()
        
        self.logger.info(
            f"Area registrada ID={area.id_area}"
        )
        
        return area
    
    def obtener_todos(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT
                id_area,
                nombre,
                descripcion
            FROM area
            ORDER BYE nombre
            """)
        
        areas = []
        
        for fila in cursor.fetchall():
            
            area = Area(
                fila.nombre,
                fila.descripcion
            )
            
            area.id_area = fila.area
            areas.append(area)
            
            conn.close()
            
            return areas