class Area():
    def __init__(self, nombre, descripcion=None):
        self.id_area      = None
        self.nombre       = nombre
        self.descripcion  = descripcion
    
    def __str__(self):
        return f"[{self.id_area}] {self.nombre} {self.descripcion or '-'}"

# Convierte el objeto en un diccionario para guardarlo en JSON
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
            datos=["descripcion"])
    
        area.id_area = datos["id_area"]
        return area