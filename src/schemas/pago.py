# schemas/pago.py

from pydantic import BaseModel, Field, validator
from uuid import UUID
from typing import Optional
from datetime import datetime

# Métodos de pago válidos
METODOS_VALIDOS = {"EFECTIVO", "TARJETA", "TRANSFERENCIA", "NEQUI", "DAVIPLATA"}


# Esquema para crear pago
class PagoCreate(BaseModel):
    metodo: str = Field(..., max_length=20)
    monto: float = Field(..., gt=0)
    id_caja: UUID
    id_compra: UUID

    @validator("metodo")
    def metodo_valido(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError("El método de pago es obligatorio")
        metodo_upper = v.strip().upper()
        if metodo_upper not in METODOS_VALIDOS:
            raise ValueError(
                f"Método de pago no válido. Opciones: {', '.join(METODOS_VALIDOS)}"
            )
        return metodo_upper

    @validator("id_caja")
    def id_caja_obligatorio(cls, v):
        if v is None:
            raise ValueError("La caja registradora es obligatoria")
        return v

    @validator("id_compra")
    def id_compra_obligatorio(cls, v):
        if v is None:
            raise ValueError("La compra es obligatoria")
        return v


# Esquema para actualizar pago
class PagoUpdate(BaseModel):
    metodo: Optional[str] = Field(None, max_length=20)
    monto: Optional[float] = Field(None, gt=0)

    @validator("metodo")
    def metodo_valido_si_presente(cls, v):
        if v is not None:
            if len(v.strip()) == 0:
                raise ValueError("El método de pago no puede estar vacío")
            metodo_upper = v.strip().upper()
            if metodo_upper not in METODOS_VALIDOS:
                raise ValueError(
                    f"Método de pago no válido. Opciones: {', '.join(METODOS_VALIDOS)}"
                )
            return metodo_upper
        return v


# Esquema para devolver pago
class PagoResponse(BaseModel):
    id: UUID
    metodo: str
    monto: float
    id_caja: UUID
    id_compra: UUID
    activo: bool

    class Config:
        from_attributes = True


class RespuestaAPI(BaseModel):
    mensaje: str
    exito: bool
