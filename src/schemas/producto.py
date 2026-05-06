# schemas/producto.py

from pydantic import BaseModel, Field, validator
from uuid import UUID
from typing import Optional
from datetime import datetime


# Esquema para crear producto
class ProductoCreate(BaseModel):
    nombre: str = Field(..., max_length=100)
    precio: float = Field(..., ge=0)
    stock: int = Field(..., ge=0)
    id_categoria: UUID
    id_proveedor: UUID

    @validator("nombre")
    def nombre_no_vacio(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError("El nombre del producto es obligatorio")
        return v.strip()


# Esquema para actualizar producto
class ProductoUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=100)
    precio: Optional[float] = Field(None, ge=0)
    stock: Optional[int] = Field(None, ge=0)
    id_categoria: Optional[UUID] = None
    id_proveedor: Optional[UUID] = None

    @validator("nombre")
    def nombre_no_vacio_si_presente(cls, v):
        if v is not None:
            if len(v.strip()) == 0:
                raise ValueError("El nombre del producto no puede estar vacío")
            return v.strip()
        return v


# Esquema para devolver producto
class ProductoResponse(BaseModel):
    id_producto: UUID
    nombre: str
    precio: float
    stock: int
    id_categoria: UUID
    id_proveedor: UUID
    activo: bool

    class Config:
        from_attributes = True


class RespuestaAPI(BaseModel):
    mensaje: str
    exito: bool


class RespuestaAPI(BaseModel):
    mensaje: str
    exito: bool
