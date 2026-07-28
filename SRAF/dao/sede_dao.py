from config.base_datos import obtener_conexion
from config.logger import logger
from config.sistema_config import (SedeDuplicadaError, SedeNoEncontradaError)

from modelos.sede import Sede

class SedeDAO:
    def __init__(self):
    
        self.logger = logger()
        
    def insertar(self, sede):
        #abre conexion sql
        conn = obtener_conexion()
        #cursor permite ejecutar consultas
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT nombre
            FROM sede
            WHERE nombre = ?

            """, sede.nombre
        )
        
        if cursor.fetchone():
            
            conn.close()
            
            raise SedeDuplicadaError(
                
                sede.nombre
            )
            
        cursor.execute("""
            INSERT INTO sede
            (
                nombre,
                direccion,
                ciudad
            )
            VALUES
            (
                ?,?,?
            )
            """,
            
            sede.nombre,
            sede.direccion,
            sede.ciudad
            )
        
        conn.commit()
            
            
            
    def obtener_todo(self):
        
        conn = obtener_conexion()
        
        cursor = conn.cursor()
        
        cursor.execute("""
        
                SELECT
                id_sede,
                nombre,
                direccion,
                ciudad
                FROM sede
                
                ORDER BY nombre
        """)
        #lista donde se guardan las sedes
        sedes = []
        
        for fila in cursor.fetchall():
            
            sede = Sede(
                fila.nombre,
                fila.direccion,
                fila.ciudad
            )