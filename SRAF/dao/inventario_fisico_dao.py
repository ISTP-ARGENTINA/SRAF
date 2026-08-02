from config.base_datos import obtener_conexion
from config.logger import logger
from config.sistema_config import (InventarioNoEncontradoError)
from modelos.inventario_fisico import InventarioFisico

class InventarioFisicoDAO:
    def __init__(self):
        self.logger = logger()
        
    def insertar(self, inventario):
        conn = obtener_conexion()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO inventario_fisico
            (
                anio
            )
            VALUES
            (
                ?
            )
            """, inventario.anio)
        conn.commit()
        
        cursor.execute("SELECT @@IDENTITY")
        
        inventario.id_inventario = cursor.fetchone()[0]
        
        conn.close()
        
        self.logger.info(
            f"Inventario registrado ID={inventario.id_inventario}"
        )
        
        return inventario
    
    def obtener_todos(self):
        
        conn = obtener_conexion()
        
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT
                id_inventario,
                anio,
                fecha_inicio,
                fecha_fin,
                estado
            FROM inventario_fisico
            ORDER BY anio DESC
            """)
        
        inventarios = []
        
        for fila in cursor.fetchall():
            inventario = InventarioFisico(
                fila.anio
            )
            
            inventario.id_inventario = fila.id_inventario
            inventario.fecha_inicio = fila.fecha_inicio
            inventario.fecha_fin = fila.fecha_fin
            inventario.estado = fila.estado
            inventario.append(inventario)
            
        conn.close()
        
        return inventarios
        
    def actualizar(self, id_inventario, anio=None, fecha_fin=None, estado=None):
        
        conn = obtener_conexion()
        
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT *
            FROM inventario_fisico
            WHERE id_inventario = ?
            """, id_inventario)
        
        fila = cursor.fetchone()
        
        if fila is None:
            conn.close()
            
            raise InventarioNoEncontradoError(
                id_inventario
            )
        
        nuevo_anio = anio if anio else fila.anio
        
        nueva_fecha_fin = fecha_fin if fecha_fin else fila.fecha_fin
        
        nuevo_estado = estado if estado else fila.estado
        
        cursor.execute("""
            UPDATE inventario_fisico
            SET
                anio = ?,
                fecha_fin = ?,
                estado = ?
            WHERE id_inventario = ?
            """,
            
            nuevo_anio,
            nueva_fecha_fin,
            nuevo_estado,
            id_inventario)
        
        conn.commit()
            
        conn.close()
        
        inventario = InventarioFisico(
            nuevo_anio
        )
        
        inventario.id_inventario = id_inventario
        inventario.fecha_fin = nueva_fecha_fin
        inventario.estado = nuevo_estado
        
        self.logger.info(
            f"Inventario actualizado ID={id_inventario}"
        )
        
        return inventario

    def eliminar(self, id_inventario):
        
        conn = obtener_conexion()
        
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id_inventario
            FROM inventario_fisico
            WHERE id_inventario = ?
            """, id_inventario)
        
        if cursor.fectone() is None:
            
            conn.close()
            
            raise InventarioNoEncontradoError(
                id_inventario
            )
            
        cursor.execute("""
            DELETE
            FROM inventario_fisico
            WHERE id_inventario = ?
            """, id_inventario)
        
        conn.commit()
        
        conn.close()
        
        self.logger.warning(
            f"Inventario eliminado ID={id_inventario}"
        )