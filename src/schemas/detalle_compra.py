# schemas/detalle_compra.py

from pydantic import BaseModel, Field, validator
from uuid import UUID
from typing import Optional
from datetime import datetime


# Esquema para crear detalle de compra
class DetalleCompraCreate(BaseModel):
    id_producto: UUID
    id_compra: UUID
    cantidad: int = Field(..., gt=0)
    subtotal: float = Field(..., ge=0)

    @validator("id_producto")
    def id_producto_obligatorio(cls, v):
        if v is None:
            raise ValueError("El producto es obligatorio")
        return v

    @validator("id_compra")
    def id_compra_obligatorio(cls, v):
        if v is None:
            raise ValueError("La compra es obligatoria")
        return v


# Esquema para actualizar detalle de compra
class DetalleCompraUpdate(BaseModel):
    cantidad: Optional[int] = Field(None, gt=0)
    subtotal: Optional[float] = Field(None, ge=0)


# Esquema para devolver detalle de compra
class DetalleCompraResponse(BaseModel):
    id_detalle: UUID
    id_producto: UUID
    id_compra: UUID
    cantidad: int
    subtotal: float
    activo: bool

    class Config:
        from_attributes = True


class RespuestaAPI(BaseModel):
    mensaje: str
    exito: bool
