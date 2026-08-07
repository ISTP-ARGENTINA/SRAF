# schemas/categoria_activo_schema.py
from typing import Optional
from pydantic import BaseModel, field_validator

# ──────────────────────────────────────────────────────────────
# Las validaciones de este modulo viven AQUI, dentro del propio
# schema (a diferencia de otros proyectos que las centralizan en
# una carpeta "validaciones/"). Cada @field_validator es la unica
# fuente de verdad para su campo.
# ──────────────────────────────────────────────────────────────


class CategoriaActivoCrear(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

    @field_validator("nombre")
    @classmethod
    def validar_nombre(cls, valor):
        valor = valor.strip()
        if not valor:
            raise ValueError("El nombre no puede estar vacio")
        if len(valor) < 3:
            raise ValueError("El nombre debe tener al menos 3 caracteres")
        return valor.title()

    @field_validator("descripcion")
    @classmethod
    def validar_descripcion(cls, valor):
        if valor is None:
            return valor
        valor = valor.strip()
        return valor or None


class CategoriaActivoActualizar(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None

    @field_validator("nombre")
    @classmethod
    def validar_nombre(cls, valor):
        if valor is None:
            return valor
        valor = valor.strip()
        if not valor:
            raise ValueError("El nombre no puede estar vacio")
        if len(valor) < 3:
            raise ValueError("El nombre debe tener al menos 3 caracteres")
        return valor.title()

    @field_validator("descripcion")
    @classmethod
    def validar_descripcion(cls, valor):
        if valor is None:
            return valor
        return valor.strip() or None


class CategoriaActivoRespuesta(BaseModel):
    id_categoria: int
    nombre: str
    descripcion: Optional[str] = None
