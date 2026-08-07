from typing import Optional
from pydantic import BaseModel, field_validator


class DetalleInventarioCrear(BaseModel):
    id_inventario: int
    id_activo: int
    encontrado: bool = True
    observacion: Optional[str] = None

    @field_validator("observacion")
    @classmethod
    def validar_observacion(cls, valor):
        if valor is None:
            return valor
        return valor.strip() or None


class DetalleInventarioActualizar(BaseModel):
    encontrado: Optional[bool] = None
    observacion: Optional[str] = None

    @field_validator("observacion")
    @classmethod
    def validar_observacion(cls, valor):
        if valor is None:
            return valor
        return valor.strip() or None


class DetalleInventarioRespuesta(BaseModel):
    id_detalle: int
    id_inventario: int
    id_activo: int
    encontrado: bool
    observacion: Optional[str] = None
