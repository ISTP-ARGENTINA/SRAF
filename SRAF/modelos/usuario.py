import datetime

class usuario():
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
        
    @classmethod
    def from_dict(cls, datos):
        
        usuario=cls(
            datos["nombres"],
            datos["apellidos"],
            datos["nombre_usuario"],
            datos["correo"],
            datos["contrasena"],
            datos["rol"],
            datos["estado"]
        )
        
        usuario.id = datos["id"]
        
        return usuario