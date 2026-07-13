class usuario():
    def __init__(self, nombres, apellidos, nombre_usuario ,correo , contraseña, rol, estado, fecha_creacion, ultimo_acceso ):
        self.__id_usuario       = None
        self.__nombres          = nombres
        self.__apellidos        = apellidos
        self.__nombre_usuario   = nombre_usuario
        self.__correo           = correo
        self.__contraseña       = contraseña
        self.__rol              = rol
        self.__estado           = estado
        self.__fecha_creacion   = None
        self.__ultimo_acceso    = None
        
    def __str__(self):
            return f"[{self.nombres}] {self.apellidos} {self.__nombre_usuario} {self.correo} {self.__contraseña} {self.rol} {self.estado}"