# schemas/proveedor.py

from pydantic import BaseModel, Field, validator
from uuid import UUID
from typing import Optional
from datetime import datetime


# Esquema para crear proveedor
class ProveedorCreate(BaseModel):
    nombre: str = Field(..., max_length=100)

    @validator("nombre")
    def nombre_no_vacio(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError("El nombre del proveedor es obligatorio")
        return v.strip()


# Esquema para actualizar proveedor
class ProveedorUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=100)

    @validator("nombre")
    def nombre_no_vacio_si_presente(cls, v):
        if v is not None:
            if len(v.strip()) == 0:
                raise ValueError("El nombre del proveedor no puede estar vacío")
            return v.strip()
        return v


# Esquema para devolver proveedor
class ProveedorResponse(BaseModel):
    id_proveedor: UUID
    nombre: str
    activo: bool

    class Config:
        from_attributes = True


class RespuestaAPI(BaseModel):
    mensaje: str
    exito: bool
