from typing import Optional
from pydantic import BaseModel, field_validator


class AreaCrear(BaseModel):
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
        return valor.strip() or None


class AreaActualizar(BaseModel):
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
        return valor.title()

    @field_validator("descripcion")
    @classmethod
    def validar_descripcion(cls, valor):
        if valor is None:
            return valor
        return valor.strip() or None


class AreaRespuesta(BaseModel):
    id_area: int
    nombre: str
    descripcion: Optional[str] = None
