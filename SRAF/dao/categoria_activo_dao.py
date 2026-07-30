from config.base_datos import obtener_conexion
from config.logger import logger
from config.sistema_config import (CategoriaDuplicadaError, CategoriaNoEncontradaError)

class CategoriaActivioDAO:
    def __init__(self):
        self.logger = logger()
        