# schemas/usuario_schema.py
import re
import datetime
from typing import Optional
from pydantic import BaseModel, field_validator

ESTADOS_USUARIO_VALIDOS = {"ACTIVO", "INACTIVO", "BLOQUEADO"}


class UsuarioCrear(BaseModel):
    nombres: str
    apellidos: str
    nombre_usuario: str
    correo: str
    contrasena: str
    rol: str

    @field_validator("nombres", "apellidos")
    @classmethod
    def validar_nombre_apellido(cls, valor):
        valor = valor.strip()
        if not re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñ ]+", valor):
            raise ValueError("solo se permiten letras y espacios (sin numeros)")
        return valor.title()

    @field_validator("nombre_usuario")
    @classmethod
    def validar_nombre_usuario(cls, valor):
        valor = valor.strip().lower()
        if not re.fullmatch(r"[a-z0-9._]{4,50}", valor):
            raise ValueError("el nombre de usuario debe tener 4-50 caracteres: letras, numeros, punto o guion bajo")
        return valor

    @field_validator("correo")
    @classmethod
    def validar_correo(cls, valor):
        valor = valor.strip().lower()
        if not re.fullmatch(r"[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$", valor):
            raise ValueError("el correo debe tener formato usuario@dominio.com")
        return valor

    @field_validator("contrasena")
    @classmethod
    def validar_contrasena(cls, valor):
        if len(valor) < 6:
            raise ValueError("la contraseña debe tener al menos 6 caracteres")
        return valor

    @field_validator("rol")
    @classmethod
    def validar_rol(cls, valor):
        valor = valor.strip().upper()
        if not valor:
            raise ValueError("el rol no puede estar vacio")
        return valor


class UsuarioActualizar(BaseModel):
    nombres: Optional[str] = None
    apellidos: Optional[str] = None
    correo: Optional[str] = None
    rol: Optional[str] = None

    @field_validator("nombres", "apellidos")
    @classmethod
    def validar_nombre_apellido(cls, valor):
        if valor is None:
            return valor
        valor = valor.strip()
        if not re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñ ]+", valor):
            raise ValueError("solo se permiten letras y espacios (sin numeros)")
        return valor.title()

    @field_validator("correo")
    @classmethod
    def validar_correo(cls, valor):
        if valor is None:
            return valor
        valor = valor.strip().lower()
        if not re.fullmatch(r"[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$", valor):
            raise ValueError("el correo debe tener formato usuario@dominio.com")
        return valor

    @field_validator("rol")
    @classmethod
    def validar_rol(cls, valor):
        if valor is None:
            return valor
        return valor.strip().upper()


class UsuarioCambiarEstado(BaseModel):
    estado: str

    @field_validator("estado")
    @classmethod
    def validar_estado(cls, valor):
        valor = valor.strip().upper()
        if valor not in ESTADOS_USUARIO_VALIDOS:
            opciones = ", ".join(sorted(ESTADOS_USUARIO_VALIDOS))
            raise ValueError(f"El estado debe ser uno de: {opciones}")
        return valor


# La respuesta NUNCA incluye la contraseña.
class UsuarioRespuesta(BaseModel):
    id_usuario: int
    nombres: str
    apellidos: str
    nombre_usuario: str
    correo: str
    rol: str
    estado: str
    fecha_creacion: datetime.date
    ultimo_acceso: Optional[datetime.datetime] = None