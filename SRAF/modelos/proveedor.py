class Proveedor():
    def __init__(self,numero_documento_proveedor, razon_social, telefono ,correo ):
        self.__numero_documento_proveedor   = numero_documento_proveedor
        self.__razon_social                 = razon_social
        self.__telefono                     = telefono
        self.__correo                       = correo
        
    def __str__(self):
            return f"[{self.numero_documento_proveedor}] {self.razon_social} {self.telefono} {self.correo}"