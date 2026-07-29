from config.base_datos import obtener_conexion
from config.logger import logger
from config.sistema_config import (ActivoNoencontradoError, CodigoPatrimonialDuplicadoError)
from modelos.activo import Activo

class ActivoDao:
    def __init__(self):
        self.logger = logger()
        
    def insertar(self, activo):
        conn = obtener_conexion()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT codigo_patrimonial
            FROM activo
            WHERE codigo_patrimonial = ?
            """, activo.codigo_patrimonial)
        
        if cursor.fetchone():
            conn.close()
            
            raise CodigoPatrimonialDuplicadoError(
                activo.codigo_patrimonial
            )
        
        cursor.execute("""
            INSERT INTO activo(
                codigo_patrimonial,
                marca,
                modelo,
                serie,
                tipo_comprobante,
                serie_comprobante,
                numero_comprobante,
                fecha_comprobante,
                valor_compra,
                estado,
                id_categoria,
                numero_documento_proveedor,
                id_sede,
                id_area
            )
            VALUES(
                ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?
            )
            """,
            activo.codigo_patrimonial,activo.descripcion,activo.marca,activo.modelo,activo.serie,activo.tipo_comprobante,activo.serie_comprobante,activo.numero_comprobante,activo.fecha_comprobante,activo.valor_compra,activo.estado,activo.id_categoria,activo.numero_documento_proveedor,activo.id_sede,activo.id_area)
        
        conn.commit()
        
        cursor.execute("SELECT @@ITDENTITY")
        
        activo.id_activo = cursor.fetchone()[0]
        
        conn.close()
        
        self.logger.info(
            f"Activo registrado ID={activo.id_activo}"
        )
        return activo
    
    def obtener_todos(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT
                id_activo,
                codigo_patrimonial,
                descripcion,
                marca,
                modelo,
                serie,
                tipo_comprobante,
                serie_comprobante,
                numero_comprobante,
                fecha_compra,
                valor_compra,
                estado,
                id_categoria,
                numero_documento_proveedor,
                id_sede,
                id_area
            FROM activo
            
            ORDER BY codigo_patrimonial
                
            """)
        
        activos = []
            
        for fila in cursor.fetchall():
            activo = Activo(
                fila.codigo_patrimonial,
                fila.descripcion,
                fila.marca,
                fila.modelo,
                fila.serie,
                fila.tipo_comprobante,
                fila.serie_comprobante,
                fila.numero_comprobante,
                fila.fecha_compra,
                fila.valor_compra,
                fila.estado,
                fila.id_categoria,
                fila.numero_documento_proveedor,
                fila.id_sede,
                fila.id_area
            )
            
            activo.id_activo = fila.id_activo
            
            activos.append(activo)
            
            conn.close()
            
            return activos
    