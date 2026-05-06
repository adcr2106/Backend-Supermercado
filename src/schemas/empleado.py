# src/schemas/empleado.py

from pydantic import BaseModel, Field, validator
from uuid import UUID
from typing import Optional
from datetime import datetime


# Esquema para crear empleado
class EmpleadoCreate(BaseModel):
    documento: str = Field(..., max_length=50)
    nombre: str = Field(..., max_length=100)
    salario: float = Field(..., ge=0)
    cargo: str = Field(..., max_length=50)
    contrasena: str = Field(..., max_length=20)
    telefono: Optional[str] = Field(None, max_length=20)
    correo: Optional[str] = Field(None, max_length=100)
    creado_por: Optional[str] = Field(None, max_length=100)

    @validator("documento")
    def documento_no_vacio(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError("El documento es obligatorio")
        return v.strip()

    @validator("nombre")
    def nombre_no_vacio(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError("El nombre es obligatorio")
        return v.strip()

    @validator("cargo")
    def cargo_no_vacio(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError("El cargo es obligatorio")
        return v.strip()

    @validator("contrasena")
    def contrasena_no_vacia(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError("La contraseña es obligatoria")
        return v.strip()

    @validator("correo")
    def correo_valido(cls, v):
        if v and "@" not in v:
            raise ValueError("Formato de correo inválido")
        return v.strip() if v else v


# Esquema para actualizar empleado
class EmpleadoUpdate(BaseModel):
    documento: Optional[str] = Field(None, max_length=50)
    nombre: Optional[str] = Field(None, max_length=100)
    salario: Optional[float] = Field(None, ge=0)
    cargo: Optional[str] = Field(None, max_length=50)
    contrasena: Optional[str] = Field(None, max_length=20)
    telefono: Optional[str] = Field(None, max_length=20)
    correo: Optional[str] = Field(None, max_length=100)
    actualizado_por: Optional[str] = Field(None, max_length=100)

    @validator("documento")
    def documento_no_vacio_si_presente(cls, v):
        if v is not None:
            if len(v.strip()) == 0:
                raise ValueError("El documento no puede estar vacío")
            return v.strip()
        return v

    @validator("nombre")
    def nombre_no_vacio_si_presente(cls, v):
        if v is not None:
            if len(v.strip()) == 0:
                raise ValueError("El nombre no puede estar vacío")
            return v.strip()
        return v

    @validator("cargo")
    def cargo_no_vacio_si_presente(cls, v):
        if v is not None:
            if len(v.strip()) == 0:
                raise ValueError("El cargo no puede estar vacío")
            return v.strip()
        return v

    @validator("contrasena")
    def contrasena_no_vacia_si_presente(cls, v):
        if v is not None:
            if len(v.strip()) == 0:
                raise ValueError("La contraseña no puede estar vacía")
            return v.strip()
        return v

    @validator("correo")
    def correo_valido_si_presente(cls, v):
        if v is not None:
            if "@" not in v:
                raise ValueError("Formato de correo inválido")
            return v.strip()
        return v


# Esquema para autenticación
class EmpleadoLogin(BaseModel):
    documento: str
    contrasena: str


# Esquema para devolver empleado (sin contraseña)
class EmpleadoResponse(BaseModel):
    id: UUID
    documento: str
    nombre: str
    salario: float
    cargo: str
    telefono: Optional[str]
    correo: Optional[str]
    creado_por: Optional[str]
    actualizado_por: Optional[str]
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime]
    activo: bool

    class Config:
        from_attributes = True


# Esquema común para respuestas API
class RespuestaAPI(BaseModel):
    mensaje: str
    exito: bool
