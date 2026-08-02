from config.logger import logger

class SistemaConfig:
    
    _inst = None
    
    def __new__(cls):
        
        if cls._inst is None:
            cls._inst = super().__new__(cls)
            cls._inst.nombre = "Sistema de Registro de Activos Fijos"
            cls._inst.version = "1.0"
            cls._inst.empresa = "ISTP ARGENTINA"
            cls._inst.autor = "Adrian Solorzano"
            
            logger().info(
                f"Sistema iniciado: {cls._inst.nombre}" 
                f"Version: {cls._inst.version}" 
                f"Empresa: {cls._inst.empresa}" 
                f"Autor: {cls._inst.autor}"
            )
        return cls._inst

class ActivoNoencontradoError(Exception):
    def __init__(self, id_activo):
        super().__init__(f"No se encontró el activo con ID={id_activo}")


class CodigoPatrimonialDuplicadoError(Exception):
    def __init__(self, codigo_patrimonial):
        super().__init__(f"Ya existe un activo con código patrimonial '{codigo_patrimonial}'")


class SedeDuplicadaError(Exception):
    def __init__(self, nombre):
        super().__init__(f"Ya existe una sede con nombre '{nombre}'")


class SedeNoEncontradaError(Exception):
    def __init__(self, id_sede):
        super().__init__(f"No se encontró la sede con ID={id_sede}")


class CategoriaDuplicadaError(Exception):
    def __init__(self, nombre):
        super().__init__(f"Ya existe una categoría con nombre '{nombre}'")


class CategoriaNoEncontradaError(Exception):
    def __init__(self, id_categoria):
        super().__init__(f"No se encontró la categoría con ID={id_categoria}")


class AreaDuplicidadError(Exception):
    def __init__(self, nombre):
        super().__init__(f"Ya existe un área con nombre '{nombre}'")


class AreaNoEncontradaError(Exception):
    def __init__(self, id_area):
        super().__init__(f"No se encontró el área con ID={id_area}")


class ProveedorDuplicadoError(Exception):
    def __init__(self, numero_documento_proveedor):
        super().__init__(f"Ya existe un proveedor con documento '{numero_documento_proveedor}'")


class ProveedorNoEncontradoError(Exception):
    def __init__(self, numero_documento_proveedor):
        super().__init__(f"No se encontró el proveedor con documento '{numero_documento_proveedor}'")


class InventarioNoEncontradoError(Exception):
    def __init__(self, id_inventario):
        super().__init__(f"No se encontró el inventario físico con ID={id_inventario}")
    