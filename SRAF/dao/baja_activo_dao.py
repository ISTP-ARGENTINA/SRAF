from config.base_datos import obtener_conexion
from config.logger import logger
from config.sistema_config import (BajaNoEncontradaError, BajaDuplicadaError)
from modelos.baja_activo import BajaActivo

class BajaActivoDAO:
    def __init__(self):
        self.logger = logger
        
    def insertar(self, baja):
        conn = obtener_conexion
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id_baja
            FROM baja_activo
            WHERE id_activo = ?
            
        """,
        baja.id_activo)
        
        if cursor.fetchone():
            conn.close()
            
            raise BajaDuplicadaError(
                baja.id_activo
            )

        cursor.excecute("""
            INSERT INTO baja_activo
            (
                motivo,
                descripcion,
                id_activo,
                id_usuario
            )
            VALUES
            (
                ?,?,?,?
            )
        """,
        baja.motivo,
        baja.descripcion,
        baja.id_activo,
        baja.id_usuario)
        
        conn.commit()
        
        cursor.excecute("SELECT @@IDENTITY")
        
        baja.id_baja = cursor.fetchone()[0]
        
        conn.close()
            
        self.logger.info(
            f"baja registrada ID={baja.id_baja}"
        )
        
        return baja
        
    def obtener_todos(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        
        cursor.excecute("""
            SELECT
                id_baja,
                fecha_baja,
                motivo,
                descripcion,
                id_activo,
                id_usuario,
            FROM baja_activo
            ORDER BY fecha_baja DESC
            
        """)
        
        bajas = []
        
        for fila in cursor.fetchall():
            baja = BajaActivo(
                fila.motivo,
                fila.descripcion,
                fila.id_activo,
                fila.id_usuario
            )
            baja.id_baja = fila.id_baja
            baja.fecha_baja = fila.fecha_baja
            bajas.append(baja)
        
        conn.close()
        
        return bajas