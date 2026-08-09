# dao/ajuste_activo_dao.py
from config.logger import Logger
from config.base_datos import obtener_conexion
from modelos.ajuste_activo import AjusteActivo
from config.sistema_config import AjusteNoEncontradoError, ActivoNoEncontradoError, UsuarioNoEncontradoError


class AjusteActivoDAO:
    def __init__(self, activo_dao, usuario_dao):
        self.__log = Logger()
        self.__activo_dao = activo_dao
        self.__usuario_dao = usuario_dao

    def insertar(self, ajuste):
        if not self.__activo_dao.buscar_por_id(ajuste.id_activo):
            raise ActivoNoEncontradoError(ajuste.id_activo)
        if not self.__usuario_dao.buscar_por_id(ajuste.id_usuario):
            raise UsuarioNoEncontradoError(ajuste.id_usuario)

        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO ajuste_activo (fecha, tipo_ajuste, valor_anterior, valor_nuevo, observacion, id_activo, id_usuario)
            VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id_ajuste""",
            (ajuste.fecha, ajuste.tipo_ajuste, ajuste.valor_anterior, ajuste.valor_nuevo,
             ajuste.observacion, ajuste.id_activo, ajuste.id_usuario),
        )
        ajuste.id_ajuste = cursor.fetchone()["id_ajuste"]
        conn.commit()
        cursor.close()
        conn.close()
        self.__log.info(f"Ajuste registrado: ID={ajuste.id_ajuste} para Activo={ajuste.id_activo}")
        return ajuste

    def buscar_por_id(self, id_ajuste):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ajuste_activo WHERE id_ajuste = %s", (id_ajuste,))
        fila = cursor.fetchone()
        cursor.close()
        conn.close()
        return AjusteActivo.from_dict(fila) if fila else None

    def obtener_por_activo(self, id_activo):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ajuste_activo WHERE id_activo = %s ORDER BY fecha DESC", (id_activo,))
        filas = cursor.fetchall()
        cursor.close()
        conn.close()
        return [AjusteActivo.from_dict(f) for f in filas]

    def obtener_todos(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ajuste_activo ORDER BY fecha DESC")
        filas = cursor.fetchall()
        cursor.close()
        conn.close()
        return [AjusteActivo.from_dict(f) for f in filas]

    def eliminar(self, id_ajuste):
        aj = self.buscar_por_id(id_ajuste)
        if not aj:
            raise AjusteNoEncontradoError(id_ajuste)

        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM ajuste_activo WHERE id_ajuste = %s", (id_ajuste,))
        conn.commit()
        cursor.close()
        conn.close()
        self.__log.info(f"Ajuste eliminado: ID={id_ajuste}")
        return True

    def total(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) AS total FROM ajuste_activo")
        total = cursor.fetchone()["total"]
        cursor.close()
        conn.close()
        return total