class Categoria_Activo():
    def __init__(self,nombre ,descripcion ):
        self.__id_categoria     = None
        self.__nombre           = nombre
        self.__descripcion      = descripcion
        
    def __str__(self):
            return f"[{self.id_sede}] {self.nombre} {self.descripcion}"