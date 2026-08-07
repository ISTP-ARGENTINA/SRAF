import datetime
from pydantic import BaseModel, field_validator


class BajaActivoCrear(BaseModel):
    motivo: str
    descripcion: str
    id_activo: int
    id_usuario: int

    @field_validator("motivo")
    @classmethod
    def validar_motivo(cls, valor):
        valor = valor.strip()
        if len(valor) < 3:
            raise ValueError("El motivo debe tener al menos 3 caracteres")
        return valor

    @field_validator("descripcion")
    @classmethod
    def validar_descripcion(cls, valor):
        valor = valor.strip()
        if len(valor) < 5:
            raise ValueError("La descripcion debe tener al menos 5 caracteres")
        return valor


class BajaActivoRespuesta(BaseModel):
    id_baja: int
    fecha_baja: datetime.date
    motivo: str
    descripcion: str
    id_activo: int
    id_usuario: int
