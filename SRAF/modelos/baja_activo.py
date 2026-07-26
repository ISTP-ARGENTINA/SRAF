class BajaActivo():
    def __init__(self, fecha_baja, motivo, descripcion, id_activo, id_usuario):
        self.id_baja        = None
        self.fecha_baja     = fecha_baja
        self.motivo         = motivo
        self.descripcion    = descripcion
        self.id_activo      = id_activo
        self.id_usuario     = id_usuario
        
    def __str__(self):
        return f"[{self.id_baja}] {self.fecha_baja} {self.motivo} {self.__descripcion} {self.id_activo} {self.id_usuario}"
        
    def to_dict(self):
        return{
            "id_baja":      self.id_baja,
            "fecha_baja":   self.fecha_baja,
            "motivo":       self.motivo,
            "descripcion":  self.descripcion,
            "id_activo":    self.id_activo,
            "id_usuario":   self.id_usuario
        }
            
    @classmethod
    def from_dict(cls,datos):
        baja = cls(
            datos["fecha_baja"],
            datos["motivo"],
            datos["descripcion"],
            datos["id_activo"],
            datos["id_usuario"]
        )
    
        baja.id_baja = datos["id_baja"]
    
        return baja