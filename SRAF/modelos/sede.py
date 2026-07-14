class Sede():
    def __init__(self, nombre, direccion, ciudad):
        self.id_sede      = None
        self.nombre       = nombre
        self.direccion    = direccion
        self.ciudad       = ciudad
    
    def __str__(self):
        return f"[{self.id_sede}] {self.nombre} {self.direccion} {self.ciudad}"
    
    def to_dict(self):
        
        return{
            "id": self.id_sede,
            "nombre": self.nombre,
            "direccion": self.direccion,
            "ciudad": self.ciudad
        }
        
    @classmethod
    def from_dict(cls,datos):
        
        sede = cls(
            datos["nombre"],
            datos["direccion"],
            datos["ciudad"]
        )
        
        sede.id = datos["id_sede"]
        
        return sede