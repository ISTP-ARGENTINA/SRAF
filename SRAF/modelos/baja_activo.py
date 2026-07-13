class BajaActivo():
    def __init__(self, fecha_baja, motivo, descripcion):
        self.__id_baja      = None
        self.__fecha_baja   = fecha_baja
        self.__motivo       = None
        self.__descripcion  = descripcion
        
    def __str__(self):
            return f"[{self.id_sede}] {self.fecha_baja} {self.motivo} {self.__descripcion}"