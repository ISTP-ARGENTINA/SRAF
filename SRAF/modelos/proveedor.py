class Proveedor():
# PK natural id_detalle, id_inventario,id_activo,encontrado, observacion
    def __init__(self, id_inventario, id_activo, encontrado=True, observacion=None):
        self.id_detalle = None
        self.id_inventario = id_inventario
        self.id_activo = id_activo
        self.encontrado = encontrado
        self.observacion = observacion                       
        
    def __str__(self):
            return f"[{self.id_detalle}] Inventario:{self.id_inventario} Activo:{self.id_activo} | Encontrado:{self.encontrado}"
        
    def to_dict(self):
        return{
            "id_detalle": self.id_detalle,
            "id_inventario": self.id_inventario,
            "id_activo": self.id_activo,
            "encontrado": self.encontrado,
            "observacion": self.observacion
        }
        
    @classmethod
    def from_dict(cls, datos):
        
        return cls(
            datos["id_inventario"],
            datos["id_activo"],
            datos["encontrado"],
            datos["observacion"],
        )

        detalle.id_detalle = datos ["id_detalle"]
        return detalle