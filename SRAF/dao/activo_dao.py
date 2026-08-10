# dao/activo_dao.py
import psycopg2
from config.logger import Logger
from config.base_datos import obtener_conexion
from modelos.activo import Activo
from config.sistema_config import (
    ActivoNoEncontradoError,
    CodigoPatrimonialDuplicadoError,
    SerieDuplicadaError,
    ActivoConDependenciasError,
    CategoriaNoEncontradaError,
    ProveedorNoEncontradoError,
    SedeNoEncontradaError,
    AreaNoEncontradaError,
    EstadoActivoInvalidoError,
)


class ActivoDAO:
    # Recibe los DAO de las 4 tablas maestras para validar que las FK
    # existan antes de insertar/actualizar un activo (igual que
    # ReservaDAO valida cliente_dao y tematica_dao en el otro proyecto).
    def __init__(self, categoria_dao, proveedor_dao, sede_dao, area_dao):
        self.__log = Logger()
        self.__categoria_dao = categoria_dao
        self.__proveedor_dao = proveedor_dao
        self.__sede_dao = sede_dao
        self.__area_dao = area_dao

    def insertar(self, activo):
        if not self.__categoria_dao.buscar_por_id(activo.id_categoria):
            raise CategoriaNoEncontradaError(activo.id_categoria)
        if not self.__proveedor_dao.buscar_por_id(activo.numero_documento_proveedor):
            raise ProveedorNoEncontradoError(activo.numero_documento_proveedor)
        if not self.__sede_dao.buscar_por_id(activo.id_sede):
            raise SedeNoEncontradaError(activo.id_sede)
        if not self.__area_dao.buscar_por_id(activo.id_area):
            raise AreaNoEncontradaError(activo.id_area)

        if self.buscar_por_codigo(activo.codigo_patrimonial):
            raise CodigoPatrimonialDuplicadoError(activo.codigo_patrimonial)
        if activo.serie and self.buscar_por_serie(activo.serie):
            raise SerieDuplicadaError(activo.serie)

        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO activo (
                codigo_patrimonial, descripcion, marca, modelo, serie,
                tipo_comprobante, serie_comprobante, numero_comprobante, fecha_compra,
                valor_compra, estado, id_categoria, numero_documento_proveedor, id_sede, id_area
            ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            RETURNING id_activo""",
            (activo.codigo_patrimonial, activo.descripcion, activo.marca, activo.modelo, activo.serie,
             activo.tipo_comprobante, activo.serie_comprobante, activo.numero_comprobante, activo.fecha_compra,
             activo.valor_compra, activo.estado, activo.id_categoria, activo.numero_documento_proveedor,
             activo.id_sede, activo.id_area),
        )
        activo.id_activo = cursor.fetchone()["id_activo"]
        conn.commit()
        cursor.close()
        conn.close()
        self.__log.info(f"Activo registrado: {activo.codigo_patrimonial} (ID={activo.id_activo})")
        return activo

    def buscar_por_id(self, id_activo):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM activo WHERE id_activo = %s", (id_activo,))
        fila = cursor.fetchone()
        cursor.close()
        conn.close()
        return Activo.from_dict(fila) if fila else None

    def buscar_por_codigo(self, codigo_patrimonial):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM activo WHERE codigo_patrimonial = %s", (codigo_patrimonial,))
        fila = cursor.fetchone()
        cursor.close()
        conn.close()
        return Activo.from_dict(fila) if fila else None

    def buscar_por_serie(self, serie):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM activo WHERE serie = %s", (serie,))
        fila = cursor.fetchone()
        cursor.close()
        conn.close()
        return Activo.from_dict(fila) if fila else None

    def obtener_todos(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM activo ORDER BY codigo_patrimonial")
        filas = cursor.fetchall()
        cursor.close()
        conn.close()
        return [Activo.from_dict(f) for f in filas]

    def obtener_por_sede(self, id_sede):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM activo WHERE id_sede = %s ORDER BY codigo_patrimonial", (id_sede,))
        filas = cursor.fetchall()
        cursor.close()
        conn.close()
        return [Activo.from_dict(f) for f in filas]

    def obtener_por_area(self, id_area):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM activo WHERE id_area = %s ORDER BY codigo_patrimonial", (id_area,))
        filas = cursor.fetchall()
        cursor.close()
        conn.close()
        return [Activo.from_dict(f) for f in filas]

    def actualizar(self, id_activo, descripcion=None, marca=None, modelo=None, serie=None,
                    id_categoria=None, numero_documento_proveedor=None, id_sede=None, id_area=None):
        a = self.buscar_por_id(id_activo)
        if not a:
            raise ActivoNoEncontradoError(id_activo)

        if id_categoria and not self.__categoria_dao.buscar_por_id(id_categoria):
            raise CategoriaNoEncontradaError(id_categoria)
        if numero_documento_proveedor and not self.__proveedor_dao.buscar_por_id(numero_documento_proveedor):
            raise ProveedorNoEncontradoError(numero_documento_proveedor)
        if id_sede and not self.__sede_dao.buscar_por_id(id_sede):
            raise SedeNoEncontradaError(id_sede)
        if id_area and not self.__area_dao.buscar_por_id(id_area):
            raise AreaNoEncontradaError(id_area)

        nueva_descripcion = descripcion if descripcion else a.descripcion
        nueva_marca = marca if marca is not None else a.marca
        nuevo_modelo = modelo if modelo is not None else a.modelo
        nueva_serie = serie if serie is not None else a.serie
        nueva_categoria = id_categoria if id_categoria else a.id_categoria
        nuevo_proveedor = numero_documento_proveedor if numero_documento_proveedor else a.numero_documento_proveedor
        nueva_sede = id_sede if id_sede else a.id_sede
        nueva_area = id_area if id_area else a.id_area

        if nueva_serie and nueva_serie != a.serie:
            existente = self.buscar_por_serie(nueva_serie)
            if existente and existente.id_activo != id_activo:
                raise SerieDuplicadaError(nueva_serie)

        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            """UPDATE activo SET descripcion=%s, marca=%s, modelo=%s, serie=%s,
            id_categoria=%s, numero_documento_proveedor=%s, id_sede=%s, id_area=%s
            WHERE id_activo=%s""",
            (nueva_descripcion, nueva_marca, nuevo_modelo, nueva_serie,
             nueva_categoria, nuevo_proveedor, nueva_sede, nueva_area, id_activo),
        )
        conn.commit()
        cursor.close()
        conn.close()

        a.descripcion = nueva_descripcion
        a.marca = nueva_marca
        a.modelo = nuevo_modelo
        a.serie = nueva_serie
        a.id_categoria = nueva_categoria
        a.numero_documento_proveedor = nuevo_proveedor
        a.id_sede = nueva_sede
        a.id_area = nueva_area
        self.__log.info(f"Activo actualizado: ID={id_activo}")
        return a

    def cambiar_estado(self, id_activo, nuevo_estado):
        a = self.buscar_por_id(id_activo)
        if not a:
            raise ActivoNoEncontradoError(id_activo)
        if nuevo_estado not in self.ESTADOS_VALIDOS:
            raise EstadoActivoInvalidoError(nuevo_estado)


        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("UPDATE activo SET estado=%s WHERE id_activo=%s", (nuevo_estado, id_activo))
        conn.commit()
        cursor.close()
        conn.close()

        a.estado = nuevo_estado
        self.__log.info(f"Activo ID={id_activo} cambio de estado a {nuevo_estado}")
        return a

    def eliminar(self, id_activo):
        a = self.buscar_por_id(id_activo)
        if not a:
            raise ActivoNoEncontradoError(id_activo)

        conn = obtener_conexion()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM activo WHERE id_activo = %s", (id_activo,))
            conn.commit()
        except psycopg2.errors.ForeignKeyViolation:
            conn.rollback()
            cursor.close()
            conn.close()
            self.__log.warning(f"Eliminar fallido: Activo ID={id_activo} tiene registros de inventario asociados")
            raise ActivoConDependenciasError(id_activo)

        cursor.close()
        conn.close()
        self.__log.info(f"Activo eliminado: {a.codigo_patrimonial} (ID={id_activo})")
        return True

    def total(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) AS total FROM activo")
        total = cursor.fetchone()["total"]
        cursor.close()
        conn.close()
        return total
