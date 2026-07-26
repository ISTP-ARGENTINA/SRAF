class InventarioFisico:
    def __init__(self, anio, fecha_inicio, fecha_fin, estado):
        self.id_inventario      = None
        self.anio               = anio
        self.fecha_inicio       = fecha_inicio
        self.fecha_fin          = fecha_fin
        self.estado             = estado
    
    def __str__(self):
        return f"[{self.id_inventario}] {self.anio} {self.fecha_inicio} {self.fecha_fin} {self.estado}"
        
    def to_dict(self):
        return{
            "id_inventario":    self.id_inventario,
            "anio":             self.anio,
            "fecha_inicio":     self.fecha_inicio,
            "fecha_fin":        self.fecha_fin,
            "estado":           self.estado
        }
        
    @classmethod
    def from_dict(cls,datos):
        
        inventario = cls(
            datos["anio"],
            datos["fecha_inicio"],
            datos["fecha-fin"],
            datos["estado"]
        )
        
        inventario.id_inventario = datos["id_inventario"]
        
        return inventario