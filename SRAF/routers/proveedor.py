import re
from typing import Optional
from pydantic import BaseModel, field_validator

TIPOS_DOCUMENTO_VALIDOS = {"RUC", "DNI", "CE", "PASAPORTE"}


class ProveedorCrear(BaseModel):
    numero_documento_proveedor: str
    tipo_documento: str
    razon_social: str
    telefono: Optional[str] = None
    correo: Optional[str] = None

    @field_validator("numero_documento_proveedor")
    @classmethod
    def validar_numero_documento(cls, valor):
        valor = valor.strip().upper()
        if not valor:
            raise ValueError("El numero de documento no puede estar vacio")
        if not re.fullmatch(r"[A-Z0-9\-]{5,20}", valor):
            raise ValueError("El numero de documento debe tener entre 5 y 20 caracteres alfanumericos")
        return valor

    @field_validator("tipo_documento")
    @classmethod
    def validar_tipo_documento(cls, valor):
        valor = valor.strip().upper()
        if valor not in TIPOS_DOCUMENTO_VALIDOS:
            opciones = ", ".join(sorted(TIPOS_DOCUMENTO_VALIDOS))
            raise ValueError(f"El tipo de documento debe ser uno de: {opciones}")
        return valor

    @field_validator("razon_social")
    @classmethod
    def validar_razon_social(cls, valor):
        valor = valor.strip()
        if len(valor) < 3:
            raise ValueError("La razon social debe tener al menos 3 caracteres")
        return valor

    @field_validator("telefono")
    @classmethod
    def validar_telefono(cls, valor):
        if valor is None:
            return valor
        valor = valor.strip()
        if not re.fullmatch(r"\d{6,15}", valor):
            raise ValueError("El telefono debe tener entre 6 y 15 digitos numericos")
        return valor

    @field_validator("correo")
    @classmethod
    def validar_correo(cls, valor):
        if valor is None:
            return valor
        valor = valor.strip().lower()
        if not re.fullmatch(r"[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$", valor):
            raise ValueError("El correo debe tener formato usuario@dominio.com")
        return valor


class ProveedorActualizar(BaseModel):
    tipo_documento: Optional[str] = None
    razon_social: Optional[str] = None
    telefono: Optional[str] = None
    correo: Optional[str] = None

    @field_validator("tipo_documento")
    @classmethod
    def validar_tipo_documento(cls, valor):
        if valor is None:
            return valor
        valor = valor.strip().upper()
        if valor not in TIPOS_DOCUMENTO_VALIDOS:
            opciones = ", ".join(sorted(TIPOS_DOCUMENTO_VALIDOS))
            raise ValueError(f"El tipo de documento debe ser uno de: {opciones}")
        return valor

    @field_validator("razon_social")
    @classmethod
    def validar_razon_social(cls, valor):
        if valor is None:
            return valor
        valor = valor.strip()
        if len(valor) < 3:
            raise ValueError("La razon social debe tener al menos 3 caracteres")
        return valor

    @field_validator("telefono")
    @classmethod
    def validar_telefono(cls, valor):
        if valor is None:
            return valor
        valor = valor.strip()
        if not re.fullmatch(r"\d{6,15}", valor):
            raise ValueError("El telefono debe tener entre 6 y 15 digitos numericos")
        return valor

    @field_validator("correo")
    @classmethod
    def validar_correo(cls, valor):
        if valor is None:
            return valor
        valor = valor.strip().lower()
        if not re.fullmatch(r"[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$", valor):
            raise ValueError("El correo debe tener formato usuario@dominio.com")
        return valor


class ProveedorRespuesta(BaseModel):
    numero_documento_proveedor: str
    tipo_documento: str
    razon_social: str
    telefono: Optional[str] = None
    correo: Optional[str] = None
