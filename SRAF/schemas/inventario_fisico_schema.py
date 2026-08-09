# schemas/inventario_fisico_schema.py
import datetime
from typing import Optional
from pydantic import BaseModel, field_validator

ESTADOS_INVENTARIO_VALIDOS = {"ABIERTO", "EN_PROCESO", "CERRADO"}
ANIO_MINIMO = 2020


class InventarioFisicoCrear(BaseModel):
    anio: int

    @field_validator("anio")
    @classmethod
    def validar_anio(cls, valor):
        anio_actual = datetime.date.today().year
        if valor < ANIO_MINIMO:
            raise ValueError(f"El año debe ser {ANIO_MINIMO} o posterior")
        if valor > anio_actual + 1:
            raise ValueError(f"El año no puede ser mayor a {anio_actual + 1}")
        return valor

class InventarioFisicoCerrar(BaseModel):
    fecha_fin: Optional[datetime.date] = None

    @field_validator("fecha_fin")
    @classmethod
    def validar_fecha_fin(cls,valor):
        if valor is None:
            return valor
        if valor > datetime.date.today():
            raise ValueError("La fecha de cierre no puede ser futura") 
        return valor

class InventarioFisicoRespuesta(BaseModel):
    id_inventario: int
    anio: int
    fecha_inicio: datetime.date
    fecha_fin: Optional [datetime.date] = None
    estado: str