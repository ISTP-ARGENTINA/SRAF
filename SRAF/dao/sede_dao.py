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
        
        cursor.execute("SELECT @@IDENTITY")
        
        sede.id_sede = cursor.fetchone()[0]
        
        conn.close()
        
        self.logger.info(
            f"Sede registrada ID={sede.id_sede}"
        )
        
        return sede

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
            
            sede.id_sede = fila.id_sede
            
            sedes.append(sede)
            
        conn.close()
            
        return sedes
    
    def actualizar(self, id_sede, nombre=None, direccion=None, ciudad=None):
        conn = obtener_conexion()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT *
            FROM sede
            WHERE id_sede = ?
        """, id_sede)
        
        fila = cursor.fetchone()
        
        if fila is None:
        
            conn.close()
            
            raise SedeNoEncontradaError(
                id_sede
            )
            
        nuevo_nombre = nombre if nombre else fila.nombre
        nueva_direccion = direccion if direccion else fila.direccion
        nueva_ciudad = ciudad if ciudad else fila.ciudad
        
        cursor.execute("""
            UPDATE sede
            SET
                nombre=?,
                direccion=?,
                ciudad=?
            WHERE id_sede=?
        """,
        nuevo_nombre,
        nueva_direccion,
        nueva_ciudad,
        id_sede)
        
        conn.commit()
        
        conn.close()
        
        sede = Sede(
            nuevo_nombre,
            nueva_direccion,
            nueva_ciudad
        )
        
        sede.id_sede = id_sede
        
        self.logger.info(
            
            f"Sede actualizada ID={id_sede}"
        )
        
        return sede
    
    def eliminar(self,id_sede):
        conn = obtener_conexion()
        cursor = conn.cursor()
        
        cursor.execute