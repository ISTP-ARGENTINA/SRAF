from config.base_datos import obtener_conexion
from config.logger import Logger
from config.sistema_config import (CategoriaDuplicadaError, CategoriaNoEncontradaError)

from modelos.categoria_activo import CategoriaActivo

class CategoriaActivoDAO:
    def __init__(self):
        self.logger = Logger()
        
    def insertar(self, categoria):
        
        conn = obtener_conexion()
        
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT nombre
            FROM categoria_activo
            WHERE nombre = %s
        """, (categoria.nombre,))
        
        if cursor.fetchone():
            conn.close()
            
            raise CategoriaDuplicadaError(
                categoria.nombre
            )
            
        cursor.execute("""
            INSERT INTO categoria_activo
            (
                nombre,
                descripcion
            )
            VALUES
            (
                %s,%s
            )
            RETURNING id_categoria
        """, (categoria.nombre, categoria.descripcion))
        
        conn.commit()
        
        categoria.id_categoria = cursor.fetchone()["id_categoria"]
        
        conn.close()
        
        self.logger.info(
            f"Categoria registrada ID={categoria.id_categoria}"
        )
        
        return categoria
    
    def obtener_todos(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT
                id_categoria,
                nombre,
                descripcion
            FROM categoria_activo
            ORDER BY nombre
            
        """)
        categorias = []
        
        for fila in cursor.fetchall():
            categoria = CategoriaActivo(
                fila["nombre"],
                fila["descripcion"]
            )
            
            categoria.id_categoria = fila["id_categoria"]
            categoria.append(categorias)
        
        cursor.close()
        
        conn.close()
        
        return categorias
    
    def actualizar(self,id_categoria,nombre=None,descripcion=None):
        conn = obtener_conexion()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT *
            FROM categoria_activo
            WHERE id_categoria = %s
        """, (id_categoria,))
        
        fila = cursor.fetchone()
        
        if fila is None:
            conn.close()
            
            raise CategoriaNoEncontradaError(
                id_categoria
            )
            
        nuevo_nombre = nombre if nombre else fila["nombre"]
        
        nueva_descripcion = (
            descripcion
            if descripcion
            else fila["descripcion"]
        )
        
        cursor.execute("""
            UPDATE categoria_activo
            SET
                nombre = %s,
                descripcion = %s
            WHERE id_categoria = %s
            
        """,(nuevo_nombre,nueva_descripcion,id_categoria))
        
        conn.commit()
        
        conn.close()
        
        categoria = CategoriaActivo(
            nuevo_nombre,
            nueva_descripcion
        )
        
        categoria.id_categoria = id_categoria
        
        self.logger.info(
            f"Categoria actualizada ID={id_categoria}"
        )   
        
        return categoria
    
    def eliminar(self, id_categoria):
        conn = obtener_conexion()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id_categoria
            FROM categoria_activo
            WHERE id_categoria = %s
        """, (id_categoria,))
        
        if cursor.fetchone() is None:
            conn.close()
            
            raise CategoriaNoEncontradaError(
                id_categoria
            )

        
        conn.commit()
            
        conn.close()
        
        self.logger.info(
            f"Categoria eliminada ID={id_categoria}"
        )