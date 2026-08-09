from config.base_datos import obtener_conexion
from config.logger import Logger
from config.sistema_config import (ProveedorDuplicadoError, ProveedorNoEncontradoError)
from modelos.proveedor import Proveedor


class ProveedorDAO:
    def __init__(self):
        self.logger = Logger()
    
    #INSERTAR SEDE
    def insertar(self, proveedor):
        
        #abre la conexion sqñ
        conn = obtener_conexion()
        
        #ejecuta la consulta sql
        cursor = conn.cursor()
        
        #verificara si existe el codigo de proveedor
        cursor.execute("""
            SELECT numero_documento_proveedor
            FROM proveedor
            WHERE numero_documento_proveedor = %s
        """, (proveedor.numero_documento_proveedor,))
        
        if cursor.fetchone():
            conn.close()
            
            raise ProveedorDuplicadoError(
                proveedor.numero_documento_proveedor
            )
        #procesa el registro
        cursor.execute("""
            INSERT INTO proveedor
            (
                numero_documento_proveedor,
                tipo_documento,
                razon_social,
                telefono,
                correo
            )
            
            VALUES
            (
                %s,%s,%s,%s,%s
            )
        """,
        (proveedor.numero_documento_proveedor,
        proveedor.tipo_documento,
        proveedor.razon_social,
        proveedor.telefono,
        proveedor.correo))
        
        
        #guarda el registro
        conn.commit()
        
        conn.close()
        
        self.logger.info(
            f"Proveedor registrado: "
            f"{proveedor.numero_documento_proveedor}"
        )
        
        return proveedor
    

