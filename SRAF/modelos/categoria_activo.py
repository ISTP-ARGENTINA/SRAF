class CategoriaActivo():
    def __init__(self, nombre , descripcion=None ):
        self.id_categoria     = None
        self.nombre           = nombre
        self.descripcion      = descripcion
        
    def __str__(self):
            return f"[{self.id_categoria}] {self.nombre} | {self.descripcion or '-'}"
        
    def to_dict(self):
        
        return {
            "id_categoria": self.id_categoria,
            "nombre": self.nombre,
            "descripcion": self.descripcion
            }
    @classmethod
    def from_dict(cls, datos):
        
        categoria = cls
        (datos["nombre"],
        datos["descripcion"])
        categoria.id_categoria = datos["id_categoria"]
        return categoria