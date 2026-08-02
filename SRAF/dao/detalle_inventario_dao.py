from config.base_datos import obtener_conexion
from config.logger import logger

from config.sistema_config import (DetalleInventarioDuplicadoError, DetalleInventarioNoEncontradoError)
from modelos.detalle_inventario import DetalleInventario

class DetalleInventarioDao:
    def __init__(self):
        self.logger = logger()
        
    def insertar(self, detalle):
        conn = obtener_conexion()
        cursor = conn.cursor()
        
        cursor.excecute("""
            SELECT id_detalle
            FROM detalle_inventario
            WHERE id_inventario = ?
            AND id_inventario = ?
        """,
        detalle.id_inventario,
        detalle.id_activo)
        
        if cursor.fetchone():
            conn.close()
            
            raise DetalleInventarioDuplicadoError(
                detalle.id_inventario,
                detalle.id_activo
            )
        
        cursor.execute("""
            INSERT INTO detalle_inventario
            (
                id_inventario,
                id_activo,
                encontrado,
                observado
            )
            VALUES
            (
                ?,?,?,?
            )
            """,
            detalle.id_inventario,
            detalle.id_activo,
            detalle.encontrado,
            detalle.observacion)
        
        conn.commit()
        
        cursor.execute("SELECT @@IDENTITY")
        
        detalle.id_detalle = cursor.fetchone()[0]
        
        conn.close()
        
        self.logger.info(
            f"Detalle registrado ID={detalle.id_detalle}"
        )
        
        return detalle
    
    def obtener_todos(self):
        
        conn = obtener_conexion()
        
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT
                id_detalle,
                id_inventario,
                id_activo,
                encontrado,
                observado,
            FROM detalle_inventario
            ORDER BY id_detalle
            """)
        
        detalles = []
        
        for fila in cursor.fetchall():
            detalle = DetalleInventario(
                fila.id_inventario,
                fila.id_activo,
                fila.encontrado,
                fila.observado
            )
            
            detalle.id_detalle = fila.id_detalle
            detalle.append(detalle)
            
        conn.close()
            
        return detalles