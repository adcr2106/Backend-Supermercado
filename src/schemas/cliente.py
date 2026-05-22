# schemas/cliente.py

from pydantic import BaseModel, Field, validator
from uuid import UUID
from typing import Optional


# Esquema para crear cliente
class ClienteCreate(BaseModel):
    documento: str = Field(..., max_length=50)
    nombre: str = Field(..., max_length=100)
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

    @validator("correo")
    def correo_valido(cls, v):
        if v and "@" not in v:
            raise ValueError("Formato de correo inválido")
        return v.strip() if v else v


# Esquema para actualizar cliente
class ClienteUpdate(BaseModel):
    documento: Optional[str] = Field(None, max_length=50)
    nombre: Optional[str] = Field(None, max_length=100)
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

    @validator("correo")
    def correo_valido_si_presente(cls, v):
        if v is not None:
            if "@" not in v:
                raise ValueError("Formato de correo inválido")
            return v.strip()
        return v


# Esquema para devolver cliente
class ClienteResponse(BaseModel):
    id: UUID
    documento: str
    nombre: str
    telefono: Optional[str]
    correo: Optional[str]
    creado_por: Optional[str]
    actualizado_por: Optional[str]
    activo: bool

    class Config:
        from_attributes = True


class RespuestaAPI(BaseModel):
    mensaje: str
    exito: bool
