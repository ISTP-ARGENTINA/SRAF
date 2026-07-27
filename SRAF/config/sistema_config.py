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