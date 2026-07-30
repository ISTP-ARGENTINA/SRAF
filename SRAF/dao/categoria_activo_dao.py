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
    