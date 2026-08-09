import psycopg2
from config.logger import Logger
from config.base_datos import obtener_conexion
from modelos.usuario import Usuario
from config.sistema_config import UsuarioDuplicadoError, UsuarioNoEncontradoError, UsuarioConMovimientosError


class UsuarioDAO:
    def __init__(self):
        self.__log = Logger()

    def registrar(self, usuario):
        if self.buscar_por_nombre_usuario(usuario.nombre_usuario):
            self.__log.warning(f"Usuario duplicado (nombre_usuario): {usuario.nombre_usuario}")
            raise UsuarioDuplicadoError("nombre_usuario", usuario.nombre_usuario)
        if self.buscar_por_correo(usuario.correo):
            self.__log.warning(f"Usuario duplicado (correo): {usuario.correo}")
            raise UsuarioDuplicadoError("correo", usuario.correo)

        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO usuario (nombres, apellidos, nombre_usuario, correo, "contraseña", rol, estado)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id_usuario, fecha_creacion, ultimo_acceso""",
            (usuario.nombres, usuario.apellidos, usuario.nombre_usuario,
             usuario.correo, usuario.contrasena, usuario.rol, usuario.estado),
        )
        fila = cursor.fetchone()
        usuario.id_usuario = fila["id_usuario"]
        usuario.fecha_creacion = fila["fecha_creacion"]
        usuario.ultimo_acceso = fila["ultimo_acceso"]
        conn.commit()
        cursor.close()
        conn.close()
        self.__log.info(f"Usuario registrado: {usuario.nombre_usuario} (ID={usuario.id_usuario})")
        return usuario

    def buscar_por_id(self, id_usuario):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuario WHERE id_usuario = %s", (id_usuario,))
        fila = cursor.fetchone()
        cursor.close()
        conn.close()
        return Usuario.from_dict(self.__normalizar(fila)) if fila else None

    def buscar_por_nombre_usuario(self, nombre_usuario):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuario WHERE nombre_usuario = %s", (nombre_usuario,))
        fila = cursor.fetchone()
        cursor.close()
        conn.close()
        return Usuario.from_dict(self.__normalizar(fila)) if fila else None

    def buscar_por_correo(self, correo):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuario WHERE correo = %s", (correo,))
        fila = cursor.fetchone()
        cursor.close()
        conn.close()
        return Usuario.from_dict(self.__normalizar(fila)) if fila else None

    def obtener_todos(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuario ORDER BY nombres")
        filas = cursor.fetchall()
        cursor.close()
        conn.close()
        return [Usuario.from_dict(self.__normalizar(f)) for f in filas]

    def actualizar(self, id_usuario, nombres=None, apellidos=None, correo=None, rol=None):
        u = self.buscar_por_id(id_usuario)
        if not u:
            raise UsuarioNoEncontradoError(id_usuario)

        nuevos_nombres = nombres if nombres else u.nombres
        nuevos_apellidos = apellidos if apellidos else u.apellidos
        nuevo_correo = correo if correo else u.correo
        nuevo_rol = rol if rol else u.rol

        if nuevo_correo != u.correo:
            existente = self.buscar_por_correo(nuevo_correo)
            if existente and existente.id_usuario != id_usuario:
                raise UsuarioDuplicadoError("correo", nuevo_correo)

        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE usuario SET nombres=%s, apellidos=%s, correo=%s, rol=%s WHERE id_usuario=%s",
            (nuevos_nombres, nuevos_apellidos, nuevo_correo, nuevo_rol, id_usuario),
        )
        conn.commit()
        cursor.close()
        conn.close()

        u.nombres = nuevos_nombres
        u.apellidos = nuevos_apellidos
        u.correo = nuevo_correo
        u.rol = nuevo_rol
        self.__log.info(f"Usuario actualizado: ID={id_usuario}")
        return u

    def cambiar_estado(self, id_usuario, nuevo_estado):
        u = self.buscar_por_id(id_usuario)
        if not u:
            raise UsuarioNoEncontradoError(id_usuario)

        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("UPDATE usuario SET estado=%s WHERE id_usuario=%s", (nuevo_estado, id_usuario))
        conn.commit()
        cursor.close()
        conn.close()

        u.estado = nuevo_estado
        self.__log.info(f"Usuario ID={id_usuario} cambio de estado a {nuevo_estado}")
        return u

    def eliminar(self, id_usuario):
        u = self.buscar_por_id(id_usuario)
        if not u:
            raise UsuarioNoEncontradoError(id_usuario)

        conn = obtener_conexion()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM usuario WHERE id_usuario = %s", (id_usuario,))
            conn.commit()
        except psycopg2.errors.ForeignKeyViolation:
            conn.rollback()
            cursor.close()
            conn.close()
            self.__log.warning(f"Eliminar fallido: Usuario ID={id_usuario} tiene ajustes/bajas asociadas")
            raise UsuarioConMovimientosError(id_usuario)

        cursor.close()
        conn.close()
        self.__log.info(f"Usuario eliminado: {u.nombre_usuario} (ID={id_usuario})")
        return True

    def total(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) AS total FROM usuario")
        total = cursor.fetchone()["total"]
        cursor.close()
        conn.close()
        return total

    # La columna en BD se llama "contraseña" (con ñ) pero el modelo Python
    # usa "contrasena" (sin ñ, para evitar líos de encoding en el codigo).
    # Este helper traduce la fila de la BD antes de pasarla a Usuario.from_dict().
    def __normalizar(self, fila):
        datos = dict(fila)
        datos["contrasena"] = datos.pop("contraseña")
        return datos
