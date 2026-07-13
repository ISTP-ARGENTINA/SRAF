class Area():
    def __init__(self, nombre, descripcion):
        self.__id_area      = None
        self.__nombre       = nombre
        self.__descripcion  = descripcion
    
    def __str__(self):
        return f"[{self.id_sede}] {self.nombre} {self.descripcion}"