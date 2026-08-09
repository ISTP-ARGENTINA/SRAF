import datetime

class Usuario():
    def __init__(self, nombres, apellidos, nombre_usuario ,correo , contraseña, rol, estado="ACTIVO"):
        self.id_usuario       = None
        self.nombres          = nombres
        self.apellidos        = apellidos
        self.nombre_usuario   = nombre_usuario
        self.correo           = correo
        self.contraseña       = contraseña
        self.rol              = rol
        self.estado           = estado
        self.fecha_creacion = datetime.date.today()
        self.ultimo_acceso = None

    def __str__(self):
            return f"[{self.id_usuario}] {self.nombres} {self.apellidos} | {self.nombre_usuario} | {self.correo} | {self.contraseña} | {self.rol} | {self.estado}"
    # to_dict NO incluye la contraseña: nunca debe salir en una respuesta de API.
    def to_dict(self):
        return {
            "id_usuario": self.id_usuario,
            "nombres": self.nombres,
            "apellidos": self.apellidos,
            "nombre_usuario": self.nombre_usuario,
            "correo": self.correo,
            "rol": self.rol,
            "estado": self.estado,
            "fecha_creacion": self.fecha_creacion,
            "ultimo_acceso": self.ultimo_acceso,
        }    
    @classmethod
    def from_dict(cls, datos):
        usuario = cls(
            datos["nombres"],
            datos["apellidos"],
            datos["nombre_usuario"],
            datos["correo"],
            datos["contrasena"],
            datos["rol"],
            datos["estado"],
        )
        usuario.id_usuario = datos["id_usuario"]
        usuario.fecha_creacion = datos["fecha_creacion"]
        usuario.ultimo_acceso = datos["ultimo_acceso"]
        return usuario