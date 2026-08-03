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

    def cambiar_estado(self, nuevo_estado):
        self.estado = nuevo_estado

    def __str__(self):
        return (f"[{self.id_activo}] {self.codigo_patrimonial} {self.descripcion} | "
                f"{self.marca or '-'} {self.modelo or '-'} | S/.{self.valor_compra:.2f} | {self.estado}")
    
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
            datos["codigo_patrimonial"],
            datos["descripcion"],
            datos["marca"],
            datos["modelo"],
            datos["serie"],
            datos["tipo_comprobante"],
            datos["serie_comprobante"],
            datos["numero_comprobante"],
            datos["fecha_compra"],
            datos["valor_compra"],
            datos["estado"],
            datos["id_categoria"],
            datos["numero_documento_proveedor"],
            datos["id_sede"],
            datos["id_area"],
        )

        activo.id_activo = datos["id_activo"]
        
        return activo