from config.base_datos import obtener_conexion
from config.logger import logger
from config.sistema_config import (CategoriaDuplicadaError, CategoriaNoEncontradaError)

from modelos.categoria_activo import CategoriaActivo

class CategoriaActivioDAO:
    def __init__(self):
        self.logger = logger()
        
    def insertar(self, categoria):
        
        conn = obtener_conexion()
        
        cursor = conn.cursor()
        
        cursor.excecute("""
            SELECT nombre
            FROM categoria_activo
            WHERE nombre = ?
        """, categoria.nombre)
        
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
                ?,?
            )
            """, categoria.nombre, categoria.descripcion)
        
        conn.commit()
        
        cursor.execute("SELECT @@IDENTITY")
        
        categoria.id_categoria = cursor.fetchone()[0]
        
        conn.close()
        
        
        self.looger.info(
            f"Categoria registrada ID={categoria.id_categoria}"
        )
        
        return categoria
    
    def obtener_todos(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT
                id_categoira,
                nombre,
                descripcion
            FROM categoria_activo
            ORDER BY nombre
            
            """)
        categoria = []
        
        for fila in cursor.fetchall():
            categoria = CategoriaActivo(
                fila.nombre,
                fila.descripcion
            )
            
        categoria.id_categoria = fila.id_categoria
        
        categoria.append(categoria)
        
        conn.close()
        
        return categoria
    
    def actualizar(self,id_categoria,nombre=None,descripcion=None):
        conn = obtener_conexion()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT *
            FROM categorira_activo
            WHERE id_categoria = ?
        """, id_categoria)
        
        fila = cursor.fetchone()
        
        if fila is None:
            conn.close()
            
            raise CategoriaNoEncontradaError(
                id_categoria
            )
            
        nuevo_nombre = nombre if nombre else fila.nombre
        
        nueva_descripcion = (
            descripcion
            if descripcion
            else fila.descripcion
        )
        
        cursor.execute("""
            UPDATE categoria_activo
            SET
                nombre =?,
                descripcion = ?
            WHERE id_categoria = ?
            
            """,nuevo_nombre,nueva_descripcion,id_categoria
            )
        
        conn.commit()
        
        conn.close()
        
        categoria = CategoriaActivo(
            nuevo_nombre,
            nueva_descripcion
        )
        
        self.logger.info(
            f"Categoria actualizada ID={id_categoria}"
        )   
        
        return categoria