class Area():
    def __init__(self, nombre, descripcion):
        self.id_area      = None
        self.nombre       = nombre
        self.descripcion  = descripcion
    
    def __str__(self):
        return f"[{self.id_area}] {self.nombre} {self.descripcion}"
    
    def to_dict(self):
        
        return {
            "id": self.id_area,
            "nombre": self.nombre,
            "decripcion": self.descripcion
            
        }
        
    @classmethod
    def from_dict(cls, datos):
        
        area = cls(
            datos=["nombre"],
            datos=["descripcion"]
        )
        
        area.id = datos["id_area"]
        
        return area