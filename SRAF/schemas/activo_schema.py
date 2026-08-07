# schemas/activo_schema.py
import re
import datetime
from typing import Optional
from decimal import Decimal
from pydantic import BaseModel, field_validator

ESTADOS_ACTIVO_VALIDOS = {"OPERATIVO", "EN_REPARACION", "INACTIVO", "PRESTADO"}
TIPOS_COMPROBANTE_VALIDOS = {"FACTURA", "BOLETA", "GUIA", "CONTRATO", "OTRO"}


class ActivoCrear(BaseModel):
    codigo_patrimonial: str
    descripcion: str
    marca: Optional[str] = None
    modelo: Optional[str] = None
    serie: Optional[str] = None
    tipo_comprobante: str
    serie_comprobante: str
    numero_comprobante: str
    fecha_compra: datetime.date
    valor_compra: Decimal
    id_categoria: int
    numero_documento_proveedor: str
    id_sede: int
    id_area: int

    @field_validator("codigo_patrimonial")
    @classmethod
    def validar_codigo_patrimonial(cls, valor):
        valor = valor.strip().upper()
        if not re.fullmatch(r"[A-Z0-9\-]{4,50}", valor):
            raise ValueError("El codigo patrimonial debe tener 4-50 caracteres alfanumericos (guiones permitidos)")
        return valor

    @field_validator("descripcion")
    @classmethod
    def validar_descripcion(cls, valor):
        valor = valor.strip()
        if len(valor) < 3:
            raise ValueError("La descripcion debe tener al menos 3 caracteres")
        return valor

    @field_validator("marca", "modelo")
    @classmethod
    def validar_marca_modelo(cls, valor):
        if valor is None:
            return valor
        return valor.strip() or None

    @field_validator("serie")
    @classmethod
    def validar_serie(cls, valor):
        if valor is None:
            return valor
        valor = valor.strip().upper()
        return valor or None

    @field_validator("tipo_comprobante")
    @classmethod
    def validar_tipo_comprobante(cls, valor):
        valor = valor.strip().upper()
        if valor not in TIPOS_COMPROBANTE_VALIDOS:
            opciones = ", ".join(sorted(TIPOS_COMPROBANTE_VALIDOS))
            raise ValueError(f"El tipo de comprobante debe ser uno de: {opciones}")
        return valor

    @field_validator("serie_comprobante", "numero_comprobante")
    @classmethod
    def validar_serie_numero_comprobante(cls, valor):
        valor = valor.strip()
        if not valor:
            raise ValueError("no puede estar vacio")
        return valor

    @field_validator("fecha_compra")
    @classmethod
    def validar_fecha_compra(cls, valor):
        if valor > datetime.date.today():
            raise ValueError("La fecha de compra no puede ser futura")
        return valor

    @field_validator("valor_compra")
    @classmethod
    def validar_valor_compra(cls, valor):
        if valor < 0:
            raise ValueError("El valor de compra no puede ser negativo")
        return round(valor, 2)

    @field_validator("numero_documento_proveedor")
    @classmethod
    def validar_numero_documento_proveedor(cls, valor):
        return valor.strip().upper()


class ActivoActualizar(BaseModel):
    descripcion: Optional[str] = None
    marca: Optional[str] = None
    modelo: Optional[str] = None
    serie: Optional[str] = None
    id_categoria: Optional[int] = None
    numero_documento_proveedor: Optional[str] = None
    id_sede: Optional[int] = None
    id_area: Optional[int] = None

    @field_validator("descripcion")
    @classmethod
    def validar_descripcion(cls, valor):
        if valor is None:
            return valor
        valor = valor.strip()
        if len(valor) < 3:
            raise ValueError("La descripcion debe tener al menos 3 caracteres")
        return valor

    @field_validator("serie")
    @classmethod
    def validar_serie(cls, valor):
        if valor is None:
            return valor
        return valor.strip().upper() or None

    @field_validator("numero_documento_proveedor")
    @classmethod
    def validar_numero_documento_proveedor(cls, valor):
        if valor is None:
            return valor
        return valor.strip().upper()


class ActivoCambiarEstado(BaseModel):
    estado: str

    @field_validator("estado")
    @classmethod
    def validar_estado(cls, valor):
        valor = valor.strip().upper()
        if valor not in ESTADOS_ACTIVO_VALIDOS:
            opciones = ", ".join(sorted(ESTADOS_ACTIVO_VALIDOS))
            raise ValueError(f"El estado debe ser uno de: {opciones}")
        return valor


class ActivoRespuesta(BaseModel):
    id_activo: int
    codigo_patrimonial: str
    descripcion: str
    marca: Optional[str] = None
    modelo: Optional[str] = None
    serie: Optional[str] = None
    tipo_comprobante: str
    serie_comprobante: str
    numero_comprobante: str
    fecha_compra: datetime.date
    valor_compra: Decimal
    estado: str
    id_categoria: int
    numero_documento_proveedor: str
    id_sede: int
    id_area: int