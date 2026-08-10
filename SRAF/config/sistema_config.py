# config/sistema_config.py
# PATRON SINGLETON #2 - SistemaConfig
# Centraliza la configuracion del sistema. Todos los modulos leen los
# mismos datos (nombre, version, empresa) sin pasarlos como parametros.
from config.logger import Logger


class SistemaConfig:
    _inst = None

    def __new__(cls):
        if cls._inst is None:
            cls._inst = super().__new__(cls)
            cls._inst.nombre = "Sistema de Registro de Activos Fijos"
            cls._inst.version = "1.0"
            cls._inst.empresa = "ISTP ARGENTINA"
            cls._inst.autor = "Adrian Solorzano"

            Logger().info(
                f"Sistema iniciado: {cls._inst.nombre} "
                f"Version: {cls._inst.version} "
                f"Empresa: {cls._inst.empresa} "
                f"Autor: {cls._inst.autor}"
            )
        return cls._inst


# ──────────────────────────────────────────────────────────────
# EXCEPCIONES PERSONALIZADAS — una por entidad, reutilizadas por
# los DAO y traducidas a codigos HTTP en cada router.
# ──────────────────────────────────────────────────────────────

# --- Activo ---
class ActivoNoEncontradoError(Exception):
    def __init__(self, id_activo):
        super().__init__(f"No se encontro el activo con ID={id_activo}")


class CodigoPatrimonialDuplicadoError(Exception):
    def __init__(self, codigo_patrimonial):
        super().__init__(f"Ya existe un activo con codigo patrimonial '{codigo_patrimonial}'")


class SerieDuplicadaError(Exception):
    def __init__(self, serie):
        super().__init__(f"Ya existe un activo con numero de serie '{serie}'")


class ActivoConDependenciasError(Exception):
    def __init__(self, id_activo):
        super().__init__(f"Activo ID={id_activo} no se puede eliminar: tiene registros de inventario asociados")


# --- Sede ---
class SedeDuplicadaError(Exception):
    def __init__(self, nombre):
        super().__init__(f"Ya existe una sede con nombre '{nombre}'")


class SedeNoEncontradaError(Exception):
    def __init__(self, id_sede):
        super().__init__(f"No se encontro la sede con ID={id_sede}")


class SedeConActivosError(Exception):
    def __init__(self, id_sede):
        super().__init__(f"Sede ID={id_sede} no se puede eliminar: tiene activos asociados")


# --- Categoria ---
class CategoriaDuplicadaError(Exception):
    def __init__(self, nombre):
        super().__init__(f"Ya existe una categoria con nombre '{nombre}'")


class CategoriaNoEncontradaError(Exception):
    def __init__(self, id_categoria):
        super().__init__(f"No se encontro la categoria con ID={id_categoria}")


class CategoriaConActivosError(Exception):
    def __init__(self, id_categoria):
        super().__init__(f"Categoria ID={id_categoria} no se puede eliminar: tiene activos asociados")


# --- Area ---
class AreaDuplicadaError(Exception):
    def __init__(self, nombre):
        super().__init__(f"Ya existe un area con nombre '{nombre}'")


class AreaNoEncontradaError(Exception):
    def __init__(self, id_area):
        super().__init__(f"No se encontro el area con ID={id_area}")


class AreaConActivosError(Exception):
    def __init__(self, id_area):
        super().__init__(f"Area ID={id_area} no se puede eliminar: tiene activos asociados")


# --- Proveedor ---
class ProveedorDuplicadoError(Exception):
    def __init__(self, numero_documento_proveedor):
        super().__init__(f"Ya existe un proveedor con documento '{numero_documento_proveedor}'")


class ProveedorNoEncontradoError(Exception):
    def __init__(self, numero_documento_proveedor):
        super().__init__(f"No se encontro el proveedor con documento '{numero_documento_proveedor}'")


class ProveedorConActivosError(Exception):
    def __init__(self, numero_documento_proveedor):
        super().__init__(f"Proveedor '{numero_documento_proveedor}' no se puede eliminar: tiene activos asociados")


# --- Usuario ---
class UsuarioDuplicadoError(Exception):
    def __init__(self, campo, valor):
        super().__init__(f"Ya existe un usuario con {campo} '{valor}'")


class UsuarioNoEncontradoError(Exception):
    def __init__(self, id_usuario):
        super().__init__(f"No se encontro el usuario con ID={id_usuario}")


class UsuarioConMovimientosError(Exception):
    def __init__(self, id_usuario):
        super().__init__(f"Usuario ID={id_usuario} no se puede eliminar: tiene ajustes o bajas registradas")


# --- Inventario fisico ---
class InventarioNoEncontradoError(Exception):
    def __init__(self, id_inventario):
        super().__init__(f"No se encontro el inventario fisico con ID={id_inventario}")


class InventarioCerradoError(Exception):
    def __init__(self, id_inventario):
        super().__init__(f"Inventario ID={id_inventario} ya esta cerrado, no admite nuevos escaneos")


# --- Ajuste de activo ---
class AjusteNoEncontradoError(Exception):
    def __init__(self, id_ajuste):
        super().__init__(f"No se encontro el ajuste con ID={id_ajuste}")


# --- Baja de activo ---
class BajaNoEncontradaError(Exception):
    def __init__(self, id_baja):
        super().__init__(f"No se encontro la baja con ID={id_baja}")


class ActivoYaDadoDeBajaError(Exception):
    def __init__(self, id_activo):
        super().__init__(f"El activo ID={id_activo} ya tiene una baja registrada")


# --- Detalle de inventario ---
class DetalleNoEncontradoError(Exception):
    def __init__(self, id_detalle):
        super().__init__(f"No se encontro el detalle de inventario con ID={id_detalle}")


class ActivoYaEscaneadoError(Exception):
    def __init__(self, id_inventario, id_activo):
        super().__init__(
            f"El activo ID={id_activo} ya fue escaneado en el inventario ID={id_inventario}"
        )

class DatoInvalidoError(ValueError):
    def __init__(self, campo, motivo):
        super().__init__(f"Dato invalido en '{campo}': {motivo}")
        
class DetalleInventarioDuplicadoError(Exception):
    def __init__(self, id_detalle):
        super().__init__(f"Ya existe un detalle de inventario con ID={id_detalle}")


class DetalleInventarioNoEncontradoError(Exception):
    def __init__(self, id_detalle):
        super().__init__(f"No se encontró el detalle de inventario con ID={id_detalle}")
        
class EstadoActivoInvalidoError(Exception):
    def __init__(self, estado):
        estados_validos = "OPERATIVO, EN_REPARACION, INACTIVO, PRESTADO"
        super().__init__(f"Estado de activo inválido: '{estado}'. Debe ser uno de: {estados_validos}")