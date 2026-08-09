# dao/detalle_inventario_dao.py
import psycopg2
from config.logger import Logger
from config.base_datos import obtener_conexion
from modelos.detalle_inventario import DetalleInventario
from config.sistema_config import (
    DetalleNoEncontradoError,
    ActivoYaEscaneadoError,
    InventarioNoEncontradoError,
    InventarioCerradoError,
    ActivoNoEncontradoError,
)


class DetalleInventarioDAO:
    def __init__(self, inventario_dao, activo_dao):
        self.__log = Logger()
        self.__inventario_dao = inventario_dao
        self.__activo_dao = activo_dao

    def insertar(self, detalle):
        inventario = self.__inventario_dao.buscar_por_id(detalle.id_inventario)
        if not inventario:
            raise InventarioNoEncontradoError(detalle.id_inventario)
        if inventario.estado == "CERRADO":
            raise InventarioCerradoError(detalle.id_inventario)
        if not self.__activo_dao.buscar_por_id(detalle.id_activo):
            raise ActivoNoEncontradoError(detalle.id_activo)

        conn = obtener_conexion()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """INSERT INTO detalle_inventario (id_inventario, id_activo, encontrado, observacion)
                VALUES (%s, %s, %s, %s) RETURNING id_detalle""",
                (detalle.id_inventario, detalle.id_activo, detalle.encontrado, detalle.observacion),
            )
            detalle.id_detalle = cursor.fetchone()["id_detalle"]
            conn.commit()
        except psycopg2.errors.UniqueViolation:
            conn.rollback()
            cursor.close()
            conn.close()
            raise ActivoYaEscaneadoError(detalle.id_inventario, detalle.id_activo)

        cursor.close()
        conn.close()
        self.__log.info(f"Detalle de inventario registrado: ID={detalle.id_detalle}")
        return detalle

    def buscar_por_id(self, id_detalle):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM detalle_inventario WHERE id_detalle = %s", (id_detalle,))
        fila = cursor.fetchone()
        cursor.close()
        conn.close()
        return DetalleInventario.from_dict(fila) if fila else None

    def obtener_por_inventario(self, id_inventario):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM detalle_inventario WHERE id_inventario = %s", (id_inventario,))
        filas = cursor.fetchall()
        cursor.close()
        conn.close()
        return [DetalleInventario.from_dict(f) for f in filas]

    def obtener_por_activo(self, id_activo):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM detalle_inventario WHERE id_activo = %s", (id_activo,))
        filas = cursor.fetchall()
        cursor.close()
        conn.close()
        return [DetalleInventario.from_dict(f) for f in filas]

    def actualizar(self, id_detalle, encontrado=None, observacion=None):
        d = self.buscar_por_id(id_detalle)
        if not d:
            raise DetalleNoEncontradoError(id_detalle)

        nuevo_encontrado = encontrado if encontrado is not None else d.encontrado
        nueva_observacion = observacion if observacion is not None else d.observacion

        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE detalle_inventario SET encontrado=%s, observacion=%s WHERE id_detalle=%s",
            (nuevo_encontrado, nueva_observacion, id_detalle),
        )
        conn.commit()
        cursor.close()
        conn.close()

        d.encontrado = nuevo_encontrado
        d.observacion = nueva_observacion
        self.__log.info(f"Detalle de inventario actualizado: ID={id_detalle}")
        return d

    def eliminar(self, id_detalle):
        d = self.buscar_por_id(id_detalle)
        if not d:
            raise DetalleNoEncontradoError(id_detalle)

        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM detalle_inventario WHERE id_detalle = %s", (id_detalle,))
        conn.commit()
        cursor.close()
        conn.close()
        self.__log.info(f"Detalle de inventario eliminado: ID={id_detalle}")
        return True

    def total(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) AS total FROM detalle_inventario")
        total = cursor.fetchone()["total"]
        cursor.close()
        conn.close()
        return total