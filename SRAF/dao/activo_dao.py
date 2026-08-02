from config.base_datos import obtener_conexion
from config.logger import logger
from config.sistema_config import (ActivoNoencontradoError, CodigoPatrimonialDuplicadoError)
from modelos.activo import Activo

class ActivoDao:
    def __init__(self):
        self.logger = logger()
        
    def insertar(self, activo):
        conn = obtener_conexion()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT codigo_patrimonial
            FROM activo
            WHERE codigo_patrimonial = %s
            """, activo.codigo_patrimonial)
        
        if cursor.fetchone():
            conn.close()
            
            raise CodigoPatrimonialDuplicadoError(
                activo.codigo_patrimonial
            )
        
        cursor.execute("""
            INSERT INTO activo(
                codigo_patrimonial,
                marca,
                modelo,
                serie,
                tipo_comprobante,
                serie_comprobante,
                numero_comprobante,
                fecha_comprobante,
                valor_compra,
                estado,
                id_categoria,
                numero_documento_proveedor,
                id_sede,
                id_area
            )
            VALUES(
                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
            )
            RETURNING id_activo
        """,
        activo.codigo_patrimonial,activo.descripcion,activo.marca,activo.modelo,activo.serie,activo.tipo_comprobante,activo.serie_comprobante,activo.numero_comprobante,activo.fecha_comprobante,activo.fecha_compra,         activo.valor_compra,activo.estado,activo.id_categoria,activo.numero_documento_proveedor,activo.id_sede,activo.id_area)
        
        conn.commit()
        
        cursor.execute("SELECT @@ITDENTITY")
        
        activo.id_activo = cursor.fetchone()["id_activo"]
        
        conn.close()
        
        self.logger.info(
            f"Activo registrado ID={activo.id_activo}"
        )
        return activo
    
    def obtener_todos(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT
                id_activo,
                codigo_patrimonial,
                descripcion,
                marca,
                modelo,
                serie,
                tipo_comprobante,
                serie_comprobante,
                numero_comprobante,
                fecha_compra,
                valor_compra,
                estado,
                id_categoria,
                numero_documento_proveedor,
                id_sede,
                id_area
            FROM activo
            
            ORDER BY codigo_patrimonial
                
        """)
        
        activos = []
            
        for fila in cursor.fetchall():
            activo = Activo(
                fila["codigo_patrimonial"],
                fila["descripcion"],
                fila["marca"],
                fila["modelo"],
                fila["serie"],
                fila["tipo_comprobante"],
                fila["serie_comprobante"],
                fila["numero_comprobante"],
                fila["fecha_compra"],
                fila["valor_compra"],
                fila["estado"],
                fila["id_categoria"],
                fila["numero_documento_proveedor"],
                fila["id_sede"],
                fila["id_area"]
            )
            
            activo.id_activo = fila["id_activo"]
            
            activos.append(activo)
            
            conn.close()
            
            return activos
    
    def actualizar(self,id_activo,codigo_patrimonial=None,descripcion=None,marca=None,modelo=None,serie=None,tipo_comprobante=None,serie_comprobante=None,numero_comprobante=None,fecha_compra=None,valor_compra=None,estado=None,id_categoria=None,numero_documento_proveedor=None,id_sede=None,id_area=None):
        conn = obtener_conexion()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT *
            FROM activo
            WHERE id_activo = %s
        """,(id_activo,))
        
        fila = cursor.fetchone()
        
        if fila is None:
        
            conn.close()
            
            raise ActivoNoencontradoError(id_activo)
        nuevo_codigo = codigo_patrimonial if codigo_patrimonial else fila["codigo_patrimonial"]
        nueva_descripcion = descripcion if descripcion else fila["descripcion"]
        nueva_marca = marca if marca else fila["marca"]
        nuevo_modelo = modelo if modelo else fila["modelo"]
        nueva_serie = serie if serie else fila["serie"]
        nuevo_tipo = tipo_comprobante if tipo_comprobante else fila["tipo_comprobante"]
        nueva_serie_comp = serie_comprobante if serie_comprobante else fila["serie_comprobante"]
        nuevo_numero = numero_comprobante if numero_comprobante else fila["numero_comprobante"]
        nueva_fecha = fecha_compra if fecha_compra else fila["fecha_compra"]
        nuevo_valor = valor_compra if valor_compra else fila["valor_compra"]
        nuevo_estado = estado if estado else fila["estado"]
        nueva_categoria = id_categoria if id_categoria else fila["id_categoria"]
        nuevo_proveedor = numero_documento_proveedor if numero_documento_proveedor else fila["numero_documento_proveedor"]
        nueva_sede = id_sede if id_sede else fila["id_sede"]
        nueva_area = id_area if id_area else fila["id_area"]
        
        cursor.execute("""
            UPDATE activo
            SET
                codigo_patrimonial = %s,
                descripcion = %s,
                marca = %s,
                modelo = %s,
                serie = %s,
                tipo_comprobante = %s,
                serie_comprobante = %s,
                numero_comprobante = %s,
                fecha_compra = %s,
                valor_compra = %s,
                estado = %s,
                id_categoria = %s,
                numero_documento_proveedor = %s,
                id_sede = %s,
                id_area = %s
            WHERE id_activo = %s
        """,
        (
        nuevo_codigo,nueva_descripcion,nueva_marca,    nuevo_modelo,nueva_serie,nuevo_tipo,nueva_serie_comp,nuevo_numero,nueva_fecha,nuevo_valor,nuevo_estado,nueva_categoria,nuevo_proveedor,nueva_sede,nueva_area,
        id_activo
        ))
        
        conn.commit()
        
        conn.close()
        
        activo = Activo(
            nuevo_codigo,
            nueva_descripcion,
            nueva_marca,
            nuevo_modelo,
            nueva_serie,
            nuevo_tipo,
            nueva_serie_comp,
            nuevo_numero,
            nueva_fecha,
            nuevo_valor,
            nuevo_estado,
            nueva_categoria,
            nuevo_proveedor,
            nueva_sede,
            nueva_area
        )
        
        activo.id_activo = id_activo
        
        self.logger.info(
            f"Activo actualizado ID={id_activo}"
        )
        
        return activo
    
    def eliminar(self, id_activo):
        conn = obtener_conexion()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id_activo
            FROM activo
            WHERE id_activo = %s
        """, (id_activo,))
        
        if cursor.fetchone() is None:
            conn.close()
            
            raise ActivoNoencontradoError(
                id_activo
            )
        cursor.execute("""
            DELETE
            FROM activo
            WHERE id_activo = %s
        """, (id_activo,))
        
        conn.commit()
        
        conn.close()
        
        self.logger.warning(
            f"Activo eliminado ID={id_activo}"
        )