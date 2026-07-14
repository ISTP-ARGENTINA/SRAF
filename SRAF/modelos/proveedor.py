class Proveedor():
    def __init__(self,numero_documento_proveedor, tipo_documento, razon_social, telefono ,correo ):
        self.numero_documento_proveedor     = numero_documento_proveedor
        self.tipo_documento                 = tipo_documento
        self.razon_social                   = razon_social
        self.telefono                       = telefono
        self.correo                         = correo
        
    def __str__(self):
            return f"[{self.numero_documento_proveedor}] {self.tipo_documento} {self.razon_social} {self.telefono} {self.correo}"
        
    def to_dict(self):
        return{
            "numero_documento_proveedor": self.numero_documento_proveedor,
            "tipo_documento": self.tipo_documento,
            "razon_social": self.razon_social,
            "telefono": self.telefono,
            "correo": self.correo
        }
        
    @classmethod
    def from_dict(cls, datos):
        
        return cls(
            datos["numero_documento_proveedor"],
            datos["tipo_documento"],
            datos["razon_social"],
            datos["telefono"],
            datos["correo"]
        )