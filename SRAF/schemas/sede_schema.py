# schemas/sede_schema.py
from typing import Optional
from pydantic import BaseModel, field_validator


class SedeCrear(BaseModel):
    nombre: str
    direccion: str
    ciudad: str

    @field_validator("nombre")
    @classmethod
    def validar_nombre(cls, valor):
        valor = valor.strip()
        if not valor:
            raise ValueError("El nombre no puede estar vacio")
        if len(valor) < 3:
            raise ValueError("El nombre debe tener al menos 3 caracteres")
        return valor.title()

    @field_validator("direccion")
    @classmethod
    def validar_direccion(cls, valor):
        valor = valor.strip()
        if not valor:
            raise ValueError("La direccion no puede estar vacia")
        if len(valor) < 5:
            raise ValueError("La direccion debe tener al menos 5 caracteres")
        return valor.title()

    @field_validator("ciudad")
    @classmethod
    def validar_ciudad(cls, valor):
        valor = valor.strip()
        if not valor:
            raise ValueError("La ciudad no puede estar vacia")
        return valor.title()


class SedeActualizar(BaseModel):
    nombre: Optional[str] = None
    direccion: Optional[str] = None
    ciudad: Optional[str] = None

    @field_validator("nombre")
    @classmethod
    def validar_nombre(cls, valor):
        if valor is None:
            return valor
        valor = valor.strip()
        if not valor:
            raise ValueError("El nombre no puede estar vacio")
        return valor.title()

    @field_validator("direccion")
    @classmethod
    def validar_direccion(cls, valor):
        if valor is None:
            return valor
        valor = valor.strip()
        if len(valor) < 5:
            raise ValueError("La direccion debe tener al menos 5 caracteres")
        return valor.title()

    @field_validator("ciudad")
    @classmethod
    def validar_ciudad(cls, valor):
        if valor is None:
            return valor
        return valor.strip().title()


class SedeRespuesta(BaseModel):
    id_sede: int
    nombre: str
    direccion: str
    ciudad: str
