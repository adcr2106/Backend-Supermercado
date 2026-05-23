"""
API de Empleados - Endpoints para gestión de empleados
"""

from typing import List
from uuid import UUID
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from crud.crud_empleado import EmpleadoCRUD
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from schemas.empleado import (
    EmpleadoCreate,
    EmpleadoResponse,
    EmpleadoUpdate,
    EmpleadoLogin,
    RespuestaAPI,
)
from sqlalchemy.orm import Session

router = APIRouter(prefix="/empleados", tags=["empleados"])


@router.get("/", response_model=List[EmpleadoResponse])
async def obtener_empleados(
    skip: int = 0,
    limit: int = 100,
    incluir_inactivos: bool = False,
    db: Session = Depends(get_db),
):
    """Obtener todos los empleados con paginación."""
    try:
        empleado_crud = EmpleadoCRUD(db)
        empleados = empleado_crud.obtener_empleados(
            skip=skip, limit=limit, incluir_inactivos=incluir_inactivos
        )
        return empleados
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener empleados: {str(e)}",
        )


@router.get("/{empleado_id}", response_model=EmpleadoResponse)
async def obtener_empleado(
    empleado_id: UUID,
    incluir_inactivos: bool = False,
    db: Session = Depends(get_db),
):
    """Obtener un empleado por ID."""
    try:
        empleado_crud = EmpleadoCRUD(db)
        empleado = empleado_crud.obtener_empleado(
            empleado_id, incluir_inactivos=incluir_inactivos
        )
        if not empleado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Empleado no encontrado",
            )
        return empleado
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener empleado: {str(e)}",
        )


@router.get("/documento/{documento}", response_model=EmpleadoResponse)
async def obtener_empleado_por_documento(documento: str, db: Session = Depends(get_db)):
    """Obtener un empleado por documento."""
    try:
        empleado_crud = EmpleadoCRUD(db)
        empleado = empleado_crud.obtener_empleado_por_documento(documento)
        if not empleado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Empleado no encontrado",
            )
        return empleado
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener empleado: {str(e)}",
        )


@router.get("/correo/{correo}", response_model=EmpleadoResponse)
async def obtener_empleado_por_correo(correo: str, db: Session = Depends(get_db)):
    """Obtener un empleado por correo."""
    try:
        empleado_crud = EmpleadoCRUD(db)
        empleado = empleado_crud.obtener_empleado_por_correo(correo)
        if not empleado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Empleado no encontrado",
            )
        return empleado
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener empleado: {str(e)}",
        )


@router.post("/", response_model=EmpleadoResponse, status_code=status.HTTP_201_CREATED)
async def crear_empleado(empleado_data: EmpleadoCreate, db: Session = Depends(get_db)):
    """Crear un nuevo empleado."""
    try:
        empleado_crud = EmpleadoCRUD(db)
        empleado = empleado_crud.crear_empleado(
            documento=empleado_data.documento,
            nombre=empleado_data.nombre,
            salario=empleado_data.salario,
            cargo=empleado_data.cargo,
            contrasena=empleado_data.contrasena,
            telefono=empleado_data.telefono,
            correo=empleado_data.correo,
            creado_por=(
                empleado_data.creado_por
                if hasattr(empleado_data, "creado_por")
                else None
            ),
        )
        return empleado
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear empleado: {str(e)}",
        )


@router.post("/login", response_model=EmpleadoResponse)
async def login_empleado(login_data: EmpleadoLogin, db: Session = Depends(get_db)):
    """Autenticar empleado con documento y contraseña."""
    try:
        empleado_crud = EmpleadoCRUD(db)
        empleado = empleado_crud.autenticar_empleado(
            documento=login_data.documento,
            contrasena=login_data.contrasena,
        )
        if not empleado:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Documento o contraseña incorrectos",
            )
        return empleado
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al iniciar sesión: {str(e)}",
        )


@router.put("/{empleado_id}", response_model=EmpleadoResponse)
async def actualizar_empleado(
    empleado_id: UUID,
    empleado_data: EmpleadoUpdate,
    db: Session = Depends(get_db),
):
    """Actualizar un empleado existente."""
    try:
        empleado_crud = EmpleadoCRUD(db)

        empleado_existente = empleado_crud.obtener_empleado(
            empleado_id, incluir_inactivos=True
        )
        if not empleado_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Empleado no encontrado",
            )

        campos_actualizacion = {
            k: v for k, v in empleado_data.dict().items() if v is not None
        }

        if not campos_actualizacion:
            return empleado_existente

        empleado_actualizado = empleado_crud.actualizar_empleado(
            empleado_id, **campos_actualizacion
        )
        return empleado_actualizado
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar empleado: {str(e)}",
        )


@router.delete("/{empleado_id}", response_model=RespuestaAPI)
async def eliminar_empleado(empleado_id: UUID, db: Session = Depends(get_db)):
    """Desactivar un empleado."""
    try:
        empleado_crud = EmpleadoCRUD(db)

        empleado_existente = empleado_crud.obtener_empleado(
            empleado_id, incluir_inactivos=True
        )
        if not empleado_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Empleado no encontrado",
            )

        eliminada = empleado_crud.eliminar_empleado(empleado_id)
        if eliminada:
            return RespuestaAPI(
                mensaje="Empleado desactivado exitosamente",
                exito=True,
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El empleado ya estaba inactivo",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al desactivar empleado: {str(e)}",
        )


@router.put("/{empleado_id}/activar", response_model=RespuestaAPI)
async def activar_empleado(empleado_id: UUID, db: Session = Depends(get_db)):
    """Reactivar un empleado."""
    try:
        empleado_crud = EmpleadoCRUD(db)

        empleado_existente = empleado_crud.obtener_empleado(
            empleado_id, incluir_inactivos=True
        )
        if not empleado_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Empleado no encontrado",
            )

        activada = empleado_crud.activar_empleado(empleado_id)
        if activada:
            return RespuestaAPI(
                mensaje="Empleado activado exitosamente",
                exito=True,
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El empleado ya estaba activo",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al activar empleado: {str(e)}",
        )
