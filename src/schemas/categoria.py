# schemas/categoria.py

from pydantic import BaseModel, Field, validator
from uuid import UUID
from typing import Optional


# Esquema para crear categoría
class CategoriaCreate(BaseModel):
    nombre: str = Field(..., max_length=100)

    @validator("nombre")
    def nombre_no_vacio(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError("El nombre de la categoría es obligatorio")
        return v.strip()


# Esquema para actualizar categoría
class CategoriaUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=100)

    @validator("nombre")
    def nombre_no_vacio_si_presente(cls, v):
        if v is not None:
            if len(v.strip()) == 0:
                raise ValueError("El nombre no puede estar vacío")
            return v.strip()
        return v


# Esquema para devolver categoría
class CategoriaResponse(BaseModel):
    id_categoria: UUID
    nombre: str
    activo: bool

    class Config:
        from_attributes = True


class RespuestaAPI(BaseModel):
    mensaje: str
    exito: bool
