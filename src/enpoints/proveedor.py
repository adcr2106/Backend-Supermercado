"""
API de Proveedores - Endpoints para gestión de proveedores
"""

from typing import List
from uuid import UUID
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from crud.crud_proveedor import ProveedorCRUD
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from schemas.proveedor import (
    ProveedorCreate,
    ProveedorResponse,
    ProveedorUpdate,
    RespuestaAPI,
)
from sqlalchemy.orm import Session

router = APIRouter(prefix="/proveedores", tags=["proveedores"])


@router.get("/", response_model=List[ProveedorResponse])
async def obtener_proveedores(
    skip: int = 0,
    limit: int = 100,
    incluir_inactivos: bool = False,
    db: Session = Depends(get_db),
):
    """Obtener todos los proveedores con paginación."""
    try:
        proveedor_crud = ProveedorCRUD(db)
        proveedores = proveedor_crud.obtener_proveedores(
            skip=skip, limit=limit, incluir_inactivos=incluir_inactivos
        )
        return proveedores
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener proveedores: {str(e)}",
        )


@router.get("/{proveedor_id}", response_model=ProveedorResponse)
async def obtener_proveedor(
    proveedor_id: UUID,
    incluir_inactivos: bool = False,
    db: Session = Depends(get_db),
):
    """Obtener un proveedor por ID."""
    try:
        proveedor_crud = ProveedorCRUD(db)
        proveedor = proveedor_crud.obtener_proveedor(
            proveedor_id, incluir_inactivos=incluir_inactivos
        )
        if not proveedor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Proveedor no encontrado",
            )
        return proveedor
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener proveedor: {str(e)}",
        )


@router.get("/nombre/{nombre}", response_model=ProveedorResponse)
async def obtener_proveedor_por_nombre(nombre: str, db: Session = Depends(get_db)):
    """Obtener un proveedor por nombre."""
    try:
        proveedor_crud = ProveedorCRUD(db)
        proveedor = proveedor_crud.obtener_proveedor_por_nombre(nombre)
        if not proveedor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Proveedor no encontrado",
            )
        return proveedor
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener proveedor: {str(e)}",
        )


@router.post("/", response_model=ProveedorResponse, status_code=status.HTTP_201_CREATED)
async def crear_proveedor(
    proveedor_data: ProveedorCreate, db: Session = Depends(get_db)
):
    """Crear un nuevo proveedor."""
    try:
        proveedor_crud = ProveedorCRUD(db)
        proveedor = proveedor_crud.crear_proveedor(
            nombre=proveedor_data.nombre,
        )
        return proveedor
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear proveedor: {str(e)}",
        )


@router.put("/{proveedor_id}", response_model=ProveedorResponse)
async def actualizar_proveedor(
    proveedor_id: UUID,
    proveedor_data: ProveedorUpdate,
    db: Session = Depends(get_db),
):
    """Actualizar un proveedor existente."""
    try:
        proveedor_crud = ProveedorCRUD(db)

        proveedor_existente = proveedor_crud.obtener_proveedor(
            proveedor_id, incluir_inactivos=True
        )
        if not proveedor_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Proveedor no encontrado",
            )

        campos_actualizacion = {
            k: v for k, v in proveedor_data.dict().items() if v is not None
        }

        if not campos_actualizacion:
            return proveedor_existente

        proveedor_actualizado = proveedor_crud.actualizar_proveedor(
            proveedor_id, **campos_actualizacion
        )
        return proveedor_actualizado
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar proveedor: {str(e)}",
        )


@router.delete("/{proveedor_id}", response_model=RespuestaAPI)
async def eliminar_proveedor(proveedor_id: UUID, db: Session = Depends(get_db)):
    """Desactivar un proveedor."""
    try:
        proveedor_crud = ProveedorCRUD(db)

        proveedor_existente = proveedor_crud.obtener_proveedor(
            proveedor_id, incluir_inactivos=True
        )
        if not proveedor_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Proveedor no encontrado",
            )

        eliminada = proveedor_crud.eliminar_proveedor(proveedor_id)
        if eliminada:
            return RespuestaAPI(
                mensaje="Proveedor desactivado exitosamente",
                exito=True,
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El proveedor ya estaba inactivo",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al desactivar proveedor: {str(e)}",
        )


@router.put("/{proveedor_id}/activar", response_model=RespuestaAPI)
async def activar_proveedor(proveedor_id: UUID, db: Session = Depends(get_db)):
    """Reactivar un proveedor."""
    try:
        proveedor_crud = ProveedorCRUD(db)

        proveedor_existente = proveedor_crud.obtener_proveedor(
            proveedor_id, incluir_inactivos=True
        )
        if not proveedor_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Proveedor no encontrado",
            )

        activada = proveedor_crud.activar_proveedor(proveedor_id)
        if activada:
            return RespuestaAPI(
                mensaje="Proveedor activado exitosamente",
                exito=True,
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El proveedor ya estaba activo",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al activar proveedor: {str(e)}",
        )
