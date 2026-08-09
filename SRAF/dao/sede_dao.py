import psycopg2
from config.base_datos import obtener_conexion
from config.logger import Logger
from config.sistema_config import (SedeDuplicadaError, SedeNoEncontradaError,SedeConActivosError)

from modelos.sede import Sede

class SedeDAO:
    def __init__(self):
    
        self.logger = Logger()
        
    def insertar(self, sede):
        if self.buscar_por_nombre(sede.nombre):
        #abre conexion sql
            self._log.warning(f"sede duplicada: {sede.nombre}")
            raise SedeDuplicadaError(sede.nombre)

        conn = obtener_conexion()
        #cursor permite ejecutar consultas
        cursor = conn.cursor()
        #verifica si existe la sede
        # procede con el registro de la sede
        cursor.execute("""
            INSERT INTO sede
            (
                nombre,
                direccion,
                ciudad
            )
            VALUES (%s, %s, %s) RETURNING id_sede""",
            
        (sede.nombre,sede.direccion,sede.ciudad)
        )
        
        conn.commit()
        
        cursor.close()
        
        sede.id_sede = cursor.fetchone()["id_sede"]
        
        conn.close()
        
        self._log.info(
        
            f"Sede registrada: {sede.nombre} (ID={sede.id_sede})")
        return sede

    def buscar_por_id(self, id_sede):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sede WHERE id_sede = %s", (id_sede,))
        fila = cursor.fetchone()
        cursor.close()
        conn.close()
        return Sede.from_dict(fila) if fila else None

    def buscar_por_nombre(self, nombre):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sede WHERE nombre = %s", (nombre,))
        fila = cursor.fetchone()
        cursor.close()
        conn.close()
        return Sede.from_dict(fila) if fila else None

    def obtener_todos(self):
        #obtiene todo los registros de sede
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sede ORDER BY nombre")
        filas = cursor.fetchall()
        cursor.close()
        conn.close()
        return [Sede.from_dict(f) for f in filas]
    def actualizar(self, id_sede, nombre=None, direccion=None, ciudad=None):
        s= self.buscar_por_id(id_sede)
        if not s:
            raise SedeNoEncontradaError(id_sede)

        nuevo_nombre = nombre if nombre else s.nombre
        nueva_direccion = direccion if direccion else s.direccion
        nueva_ciudad = ciudad if ciudad else s.ciudad

        if nuevo_nombre != s.nombre:
            existente= self.buscar_por_nombre(nuevo_nombre)
            if existente and existente.id_sede != id_sede:
                raise SedeNoEncontradaError(id_sede)
        conn = obtener_conexion()
        cursor = conn.cursor()
        #busca la sede por id si existe
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
        #registra la sede
        cursor.execute("""
            UPDATE sede
            SET
                nombre=%s,
                direccion=%s,
                ciudad=%s
            WHERE id_sede=%s
        """,
        (nuevo_nombre,
        nueva_direccion,
        nueva_ciudad,
        id_sede))
        
        conn.commit()
        conn.close()
        cursor.close()
        
        s.nombre= nuevo_nombre
        s.direccion= nueva_direccion
        s.ciudad= nueva_ciudad
        
        self.logger.info(
            
            f"Sede actualizada ID={id_sede}"
        )
        
        return s
    
    def eliminar(self,id_sede):
        s= self.buscar_por_id (id_sede)
        if not s:
            raise SedeNoEncontradaError(id_sede)
# Tomar encuenta que s es la abreviatura de Sede       
        conn = obtener_conexion()
        cursor = conn.cursor()
        #busca la sede por id para eliminarla
        try:
            cursor.execute("DELETE FROM sede WHERE id_sede = %s", (id_sede,))
            conn.commit()
        except psycopg2.errors.ForeignKeyViolation:   
            conn.rollback()
            cursor.close()
            conn.close()
            self.__log.warning(f"Eliminar fallido: Sede ID={id_sede} tiene activos asociados")
            raise SedeConActivosError(id_sede)
            
        cursor.close()
        conn.close()
        self.__log.info(f"Sede eliminada: {s.nombre} (ID={id_sede})")
        return True
    
    def total(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) AS total FROM sede")
        total = cursor.fetchone()["total"]
        cursor.close()
        conn.close()
        return total
        