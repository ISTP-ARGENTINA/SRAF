import psycopg2
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
        
    def actualizar(self,id_area,nombre=None,descripcion=None):
        conn = obtener_conexion()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT *
            FROM area
            WHERE id_area = ?
            
        """, id_area)
        
        fila = cursor.fetchone()
        
        if fila is None:
            
            conn.close()
            
            raise AreaNoEncontradaError(
                id_area
            )
            
        nuevo_nombre = nombre if nombre else fila.nombre
        
        nueva_descripcion = (
            descripcion
            if descripcion
            else fila.descripcion
        )
        
        cursor.execute("""
            UPDATE area
            SET
                nombre = ?,
                descripcion = ?
            WHERE id_area = ?
        """, nuevo_nombre, nueva_descripcion, id_area)
        
        conn.commit
        
        conn.close()
        
        area = Area(
            nuevo_nombre,
            nueva_descripcion
        )
        
        area.id_area = id_area
        
        self.looger.info(
            f"Area actualizada ID={id_area}"
        )
        
        return area
    
    def eliminar(self, id_area):
        conn = obtener_conexion()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELEC id_area
            FROM area
            WHERE id_area = ?
        """, id_area)
        
        if cursor.fetchone() is None:
            conn.close()
            
            raise AreaNoEncontradaError(
                id_area
            )
        cursor.execute("""
            DELETE
            FROM area
            WHERE id_area = ?
        """, id_area)
        
        conn.commit()
        
        conn.close()
        
        self.logger.warning(
            f"Area eliminada ID={id_area}"
        )
        