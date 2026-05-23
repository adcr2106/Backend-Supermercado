# schemas/compra.py

from pydantic import BaseModel, Field, validator
from uuid import UUID
from typing import Optional
from datetime import datetime


# Esquema para crear compra
class CompraCreate(BaseModel):
    total: float = Field(0, ge=0)
    doc_cliente: str = Field(..., min_length=1, max_length=50)
    doc_empleado: str = Field(..., min_length=1, max_length=50)

    @validator("doc_cliente")
    def doc_cliente_no_vacio(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError("El documento del cliente es obligatorio")
        return v.strip()

    @validator("doc_empleado")
    def doc_empleado_no_vacio(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError("El documento del empleado es obligatorio")
        return v.strip()


# Esquema para actualizar compra
class CompraUpdate(BaseModel):
    total: Optional[float] = Field(None, ge=0)
    doc_cliente: Optional[str] = Field(None, max_length=50)
    doc_empleado: Optional[str] = Field(None, max_length=50)

    @validator("doc_cliente")
    def doc_cliente_no_vacio_si_presente(cls, v):
        if v is not None:
            if len(v.strip()) == 0:
                raise ValueError("El documento del cliente no puede estar vacío")
            return v.strip()
        return v

    @validator("doc_empleado")
    def doc_empleado_no_vacio_si_presente(cls, v):
        if v is not None:
            if len(v.strip()) == 0:
                raise ValueError("El documento del empleado no puede estar vacío")
            return v.strip()
        return v


# Esquema para devolver compra
class CompraResponse(BaseModel):
    id: UUID
    total: float
    doc_cliente: str
    doc_empleado: str
    fecha_hora: datetime
    activo: bool

    class Config:
        from_attributes = True


class RespuestaAPI(BaseModel):
    mensaje: str
    exito: bool
