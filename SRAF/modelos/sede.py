class Sede():
    def __init__(self, nombre, direccion, ciudad):
        self.__id_sede      = None
        self.__nombre       = nombre
        self.__direccion    = direccion
        self.__ciudad       = ciudad
    
    def __str__(self):
        return f"[{self.id_sede}] {self.nombre} {self.direccion} {self.ciudad}"