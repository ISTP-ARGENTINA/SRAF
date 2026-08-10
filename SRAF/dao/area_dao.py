import psycopg2
from config.base_datos import obtener_conexion
from config.logger import Logger
from config.sistema_config import (AreaDuplicadaError, AreaNoEncontradaError)
from modelos.area import Area

class AreaDAO:
    
    def __init__(self):
        self.logger = Logger()
        
    def insertar(self, area):
        conn = obtener_conexion()
        cursor = conn.cursor()
        #ejecuta la consulta sql y valida si ahi duplicidad
        cursor.execute("""
            SELECT nombre
            FROM area
            WHERE nombre = %s            
        """, (area.nombre,))
        if cursor.fetchone():
            
            cursor.close()
            
            conn.close()
            
            raise AreaDuplicadaError(
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
                %s,%s
            )
            RETURNING id_area
        """,
        (area.nombre, area.descripcion)
        )
        
        conn.commit()
        
        area.id_area = cursor.fetchone()["id_area"]
        
        cursor.close()
        
        conn.close()
        
        self.logger.info(
            f"Area registrada ID={area.id_area}"
        )
        
        return area
    
    def buscar_por_id(self, id_area):
        conn = obtener_conexion()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id_area, nombre, descripcion
            FROM area
            WHERE id_area = %s
        """, (id_area,))
        
        fila = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if fila is None:
            return None
        
        area = Area(fila["nombre"], fila["descripcion"])
        area.id_area = fila["id_area"]
        
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
            ORDER BY nombre
        """)
        
        areas = []
        
        for fila in cursor.fetchall():
            
            area = Area(
                fila["nombre"],
                fila["descripcion"]
            )
            
            area.id_area = fila["id_area"]
            areas.append(area)
            
        cursor.close()
        
        conn.close()
            
        return areas
        
    def actualizar(self,id_area,nombre=None,descripcion=None):
        conn = obtener_conexion()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT *
            FROM area
            WHERE id_area = %s
            
        """, (id_area,))
        
        fila = cursor.fetchone()
        
        if fila is None:
            
            cursor.close()
            
            conn.close()
            
            raise AreaNoEncontradaError(
                id_area
            )
            
        nuevo_nombre = nombre if nombre else fila["nombre"]
        
        nueva_descripcion = (
            descripcion
            if descripcion
            else fila["descripcion"]
        )
        
        cursor.execute("""
            UPDATE area
            SET
                nombre = %s,
                descripcion = %s
            WHERE id_area = %s
        """, (nuevo_nombre, nueva_descripcion, id_area))
        
        conn.commit()
        
        cursor.close()
        
        conn.close()
        
        area = Area(
            nuevo_nombre,
            nueva_descripcion
        )
        
        area.id_area = id_area
        
        self.logger.info(
            f"Area actualizada ID={id_area}"
        )
        
        return area
    
    def eliminar(self, id_area):
        conn = obtener_conexion()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id_area
            FROM area
            WHERE id_area = %s
        """, (id_area,))
        
        if cursor.fetchone() is None:
            
            cursor.close()
            
            conn.close()
            
            raise AreaNoEncontradaError(
                id_area
            )
        cursor.execute("""
            DELETE
            FROM area
            WHERE id_area = %s
        """, (id_area,))
        
        conn.commit()
        
        conn.close()
        
        self.logger.warning(
            f"Area eliminada ID={id_area}"
        )
        