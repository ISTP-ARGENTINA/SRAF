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
            cursor.close()
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
        
        cursor.close()
        
        conn.close()
        
        self.logger.info(
            f"Proveedor registrado: "
            f"{proveedor.numero_documento_proveedor}"
        )
        
        return proveedor
    
    def obtener_todos(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT
                numero_documento_proveedor,
                tipo_documento,
                razon_social,
                telefono,
                correo
            FROM proveedor
            ORDER BY razon_social
        """)
        
        proveedores = []
        
        for fila in cursor.fetchall():
            proveedor = Proveedor(
                fila["numero_documento_proveedor"],
                fila["tipo_documento"],
                fila["razon_social"],
                fila["telefono"],
                fila["correo"]
            )
            proveedores.append(proveedor)
        
        cursor.close()
        conn.close()
        
        return proveedores
    
    def buscar_por_id(self, numero_documento_proveedor):
        conn = obtener_conexion()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT
                numero_documento_proveedor,
                tipo_documento,
                razon_social,
                telefono,
                correo
            FROM proveedor
            WHERE numero_documento_proveedor = %s
        """, (numero_documento_proveedor,))
        
        fila = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if fila is None:
            return None
        
        proveedor = Proveedor(
            fila["numero_documento_proveedor"],
            fila["tipo_documento"],
            fila["razon_social"],
            fila["telefono"],
            fila["correo"]
        )
        return proveedor
    
    def actualizar(self, numero_documento_proveedor, tipo_documento=None, razon_social=None, telefono=None, correo=None):
        conn = obtener_conexion()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT *
            FROM proveedor
            WHERE numero_documento_proveedor = %s
        """, (numero_documento_proveedor,))
        
        fila = cursor.fetchone()
        
        if fila is None:
            cursor.close()
            conn.close()
            
            raise ProveedorNoEncontradoError(
                numero_documento_proveedor
            )
        
        nuevo_tipo_documento = tipo_documento if tipo_documento is not None else fila["tipo_documento"]
        nueva_razon_social = razon_social if razon_social is not None else fila["razon_social"]
        nuevo_telefono = telefono if telefono is not None else fila["telefono"]
        nuevo_correo = correo if correo is not None else fila["correo"]
        
        cursor.execute("""
            UPDATE proveedor
            SET
                tipo_documento = %s,
                razon_social = %s,
                telefono = %s,
                correo = %s
            WHERE numero_documento_proveedor = %s
        """, (nuevo_tipo_documento, nueva_razon_social, nuevo_telefono, nuevo_correo, numero_documento_proveedor))
        
        conn.commit()
        
        cursor.close()
        conn.close()
        
        proveedor = Proveedor(
            numero_documento_proveedor,
            nuevo_tipo_documento,
            nueva_razon_social,
            nuevo_telefono,
            nuevo_correo
        )
        
        self.logger.info(
            f"Proveedor actualizado: {numero_documento_proveedor}"
        )
        
        return proveedor
    
    def eliminar(self, numero_documento_proveedor):
        conn = obtener_conexion()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT numero_documento_proveedor
            FROM proveedor
            WHERE numero_documento_proveedor = %s
        """, (numero_documento_proveedor,))
        
        if cursor.fetchone() is None:
            cursor.close()
            conn.close()
            
            raise ProveedorNoEncontradoError(
                numero_documento_proveedor
            )
        
        try:
            cursor.execute("""
                DELETE
                FROM proveedor
                WHERE numero_documento_proveedor = %s
            """, (numero_documento_proveedor,))
            
            conn.commit()
        except psycopg2.errors.ForeignKeyViolation:
            conn.rollback()
            cursor.close()
            conn.close()
            
            self.logger.warning(
                f"Eliminar fallido: Proveedor {numero_documento_proveedor} tiene activos asociados"
            )
            
            raise ProveedorConActivosError(numero_documento_proveedor)
        
        cursor.close()
        conn.close()
        
        self.logger.info(
            f"Proveedor eliminado: {numero_documento_proveedor}"
        )
