# schemas/jornada.py

from pydantic import BaseModel, Field, validator
from uuid import UUID
from typing import Optional
from datetime import datetime


# Esquema para crear jornada
class JornadaCreate(BaseModel):
    id_empleado: UUID
    id_caja: UUID

    @validator("id_empleado")
    def id_empleado_obligatorio(cls, v):
        if v is None:
            raise ValueError("El empleado es obligatorio")
        return v

    @validator("id_caja")
    def id_caja_obligatorio(cls, v):
        if v is None:
            raise ValueError("La caja registradora es obligatoria")
        return v


# Esquema para actualizar jornada
class JornadaUpdate(BaseModel):
    fin_jornada: Optional[datetime] = None

    @validator("fin_jornada")
    def fin_despues_del_inicio(cls, v, values):
        if v is not None and "inicio_jornada" in values:
            inicio = values["inicio_jornada"]
            if inicio and v < inicio:
                raise ValueError("El fin de jornada no puede ser anterior al inicio")
        return v


# Esquema para devolver jornada
class JornadaResponse(BaseModel):
    id: UUID
    id_empleado: UUID
    id_caja: UUID
    inicio_jornada: datetime
    fin_jornada: Optional[datetime]
    activo: bool

    class Config:
        from_attributes = True


class RespuestaAPI(BaseModel):
    mensaje: str
    exito: bool
