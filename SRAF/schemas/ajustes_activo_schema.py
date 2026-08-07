import datetime
from pydantic import BaseModel, field_validator

TIPOS_AJUSTE_VALIDOS = {"INCREMENTO", "DISMINUCION", "CORRECCION"}


class AjusteActivoCrear(BaseModel):
    tipo_ajuste: str
    valor_anterior: str
    valor_nuevo: str
    observacion: str
    id_activo: int
    id_usuario: int

    @field_validator("tipo_ajuste")
    @classmethod
    def validar_tipo_ajuste(cls, valor):
        valor = valor.strip().upper()
        if valor not in TIPOS_AJUSTE_VALIDOS:
            opciones = ", ".join(sorted(TIPOS_AJUSTE_VALIDOS))
            raise ValueError(f"El tipo de ajuste debe ser uno de: {opciones}")
        return valor

    @field_validator("valor_anterior", "valor_nuevo")
    @classmethod
    def validar_valores(cls, valor):
        valor = valor.strip()
        if not valor:
            raise ValueError("no puede estar vacio")
        return valor

    @field_validator("observacion")
    @classmethod
    def validar_observacion(cls, valor):
        valor = valor.strip()
        if len(valor) < 5:
            raise ValueError("La observacion debe tener al menos 5 caracteres")
        return valor


class AjusteActivoRespuesta(BaseModel):
    id_ajuste: int
    fecha: datetime.datetime
    tipo_ajuste: str
    valor_anterior: str
    valor_nuevo: str
    observacion: str
    id_activo: int
    id_usuario: int