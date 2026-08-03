from config.base_datos import obtener_conexion
from config.logger import logger
from config.sistema_config import AjusteNoEncontradoError
from modelos.ajuste_activo import AjusteActivo

class AjusteActivoDAO:
    def __init__(self):
        self.logger = logger
        
    def insertar(self, ajuste):
        conn = obtener_conexion
        cursor = conn.cursor()
        cursor.execute("""
            
            INSERT INTO ajuste_activo
            (        
                tipo_ajuste,
                valor_acterior,
                valor_nuevo,
                observacion,
                id_activo,
                id_usuario,
            )
            VALUES
            (
                ?,?,?,?,?,?
            )
        """,
        ajuste.tipo_ajuste,
        ajuste.valor_anterior,
        ajuste.valor_nuevo,
        ajuste.observacion,
        ajuste.id_activo,
        ajuste.id_usuario)
            
        conn.commit()
        
        cursor.execute("SELECT @@IDENTITY")
        
        ajuste.id_ajuste = cursor.fetchone()[0]
        
        conn.close()
        
        self.logger.info(
            f"Ajuste registrado ID={ajuste.id_ajuste}"
        )
        
        return ajuste
    
    def obtener_todos(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                id_ajuste,
                fecha,
                tipo_ajuste,
                valor_anterior,
                valor_nuevo,
                observacion,
                id_activo,
                id_usuario
            FROM ajuste_activo
            ORDER BY fecha DESC
        """)
        
        ajustes = []
        
        for fila in cursor.fetchall():
            ajuste = AjusteActivo(
                fila.tipo_ajuste,
                fila.valor_anterior,
                fila.valor_nuevo,
                fila.observacion,
                fila.id_activo,
                fila.id_usuario
            )
            
            ajuste.id_ajuste = fila.id_adjuste
            ajuste.fecha = fila.fecha
            ajuste.append(ajuste)
        
        conn.close()
        
        return ajustes