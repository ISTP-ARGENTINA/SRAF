class Activo():
    def __init__(self,codigo_patrimonial, descripcion, marca, modelo, serie, tipo_comprobante, serie_comprobante, numero_comprobante, fecha_compra ,valor_compra, estado, id_categoria, numero_documento_proveedor, id_sede, id_area):
        self.id_activo                  = None
        self.codigo_patrimonial         = codigo_patrimonial
        self.descripcion                = descripcion
        self.marca                      = marca
        self.modelo                     = modelo
        self.serie                      = serie
        self.tipo_comprobante           = tipo_comprobante
        self.serie_comprobante          = serie_comprobante
        self.numero_comprobante         = numero_comprobante
        self.fecha_compra               = fecha_compra
        self.valor_compra               = valor_compra
        self.estado                     = estado
        self.id_categoria               = id_categoria
        self.numero_documento_proveedor = numero_documento_proveedor
        self.id_sede                    = id_sede
        self.id_area                    = id_area
        
    def __str__(self):
        return f"[{self.id_activo}] {self.codigo_patrimonial} {self.descripcion} {self.marca} {self.modelo} {self.serie} {self.tipo_comprobante} {self.serie_comprobante} {self.numero_comprobante} {self.fecha_compra} {self.valor_compra} {self.estado} {self.id_categoria} {self.numero_documento_proveedor} {self.id_sede} {self.id_area}"
    
    def to_dict(self):
        return{
        "id_activo": self.id_activo,
        "codigo_patrimonial": self.codigo_patrimonial,
        "descripcion": self.descripcion,
        "marca": self.marca,
        "modelo": self.modelo,
        "serie": self.serie,
        "tipo_comprobante": self.tipo_comprobante,
        "serie_comprobante": self.serie_comprobante,
        "numero_comprobante": self.numero_comprobante,
        "fecha_compra": self.fecha_compra,
        "valor_compra": self.valor_compra,
        "estado": self.estado,
        "id_categoria": self.id_categoria,
        "numero_documento_proveedor": self.numero_documento_proveedor,
        "id_sede": self.id_sede,
        "id_area": self.id_area
        }
        
@classmethod
def from_dict(cls,datos):
    
    activo = cls(
        datos[""],
        datos[""],
        datos[""],
        datos[""],
        datos[""],
        datos[""],
        datos[""],
        datos[""],
        datos[""],
        datos[""],
        datos[""],
        datos[""],
        datos[""],
        datos[""],
        datos[""],
        datos[""],
    )
    