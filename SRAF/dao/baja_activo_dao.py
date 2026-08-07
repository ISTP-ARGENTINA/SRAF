# dao/baja_activo_dao.py
from config.logger import Logger
from config.base_datos import obtener_conexion
from modelos.baja_activo import BajaActivo
from config.sistema_config import (
    BajaNoEncontradaError,
    ActivoYaDadoDeBajaError,
    ActivoNoEncontradoError,
    UsuarioNoEncontradoError,
)


class BajaActivoDAO:
    def __init__(self, activo_dao, usuario_dao):
        self.__log = Logger()
        self.__activo_dao = activo_dao
        self.__usuario_dao = usuario_dao

    def insertar(self, baja):
        if not self.__activo_dao.buscar_por_id(baja.id_activo):
            raise ActivoNoEncontradoError(baja.id_activo)
        if not self.__usuario_dao.buscar_por_id(baja.id_usuario):
            raise UsuarioNoEncontradoError(baja.id_usuario)
        if self.buscar_por_activo(baja.id_activo):
            raise ActivoYaDadoDeBajaError(baja.id_activo)

        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO baja_activo (fecha_baja, motivo, descripcion, id_activo, id_usuario)
            VALUES (%s, %s, %s, %s, %s) RETURNING id_baja""",
            (baja.fecha_baja, baja.motivo, baja.descripcion, baja.id_activo, baja.id_usuario),
        )
        baja.id_baja = cursor.fetchone()["id_baja"]
        conn.commit()
        cursor.close()
        conn.close()

        # Una baja definitiva deja el activo INACTIVO automaticamente.
        self.__activo_dao.cambiar_estado(baja.id_activo, "INACTIVO")

        self.__log.info(f"Baja registrada: ID={baja.id_baja} para Activo={baja.id_activo}")
        return baja

    def buscar_por_id(self, id_baja):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM baja_activo WHERE id_baja = %s", (id_baja,))
        fila = cursor.fetchone()
        cursor.close()
        conn.close()
        return BajaActivo.from_dict(fila) if fila else None

    def buscar_por_activo(self, id_activo):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM baja_activo WHERE id_activo = %s", (id_activo,))
        fila = cursor.fetchone()
        cursor.close()
        conn.close()
        return BajaActivo.from_dict(fila) if fila else None

    def obtener_todos(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM baja_activo ORDER BY fecha_baja DESC")
        filas = cursor.fetchall()
        cursor.close()
        conn.close()
        return [BajaActivo.from_dict(f) for f in filas]

    def eliminar(self, id_baja):
        b = self.buscar_por_id(id_baja)
        if not b:
            raise BajaNoEncontradaError(id_baja)

        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM baja_activo WHERE id_baja = %s", (id_baja,))
        conn.commit()
        cursor.close()
        conn.close()
        self.__log.info(f"Baja eliminada: ID={id_baja}")
        return True

    def total(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) AS total FROM baja_activo")
        total = cursor.fetchone()["total"]
        cursor.close()
        conn.close()
        return total
