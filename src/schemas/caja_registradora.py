from pydantic import BaseModel
from uuid import UUID
from typing import Optional


# Esquema para respuesta al cliente
class CajaRegistradoraResponse(BaseModel):
    id: UUID
    activo: bool

    class Config:
        from_attributes = True


class RespuestaAPI(BaseModel):
    mensaje: str
    exito: bool
