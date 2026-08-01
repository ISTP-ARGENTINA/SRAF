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
        
        