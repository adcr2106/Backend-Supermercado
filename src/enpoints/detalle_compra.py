"""
API de DetalleCompra - Endpoints para gestión de detalles de compra
"""

from typing import List
from uuid import UUID
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from crud.crud_detalle_compra import DetalleCompraCRUD
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from schemas.detalle_compra import (
    DetalleCompraCreate,
    DetalleCompraResponse,
    DetalleCompraUpdate,
    RespuestaAPI,
)
from sqlalchemy.orm import Session

router = APIRouter(prefix="/detalle-compras", tags=["detalle_compras"])


@router.get("/", response_model=List[DetalleCompraResponse])
async def obtener_detalles(
    skip: int = 0,
    limit: int = 100,
    incluir_inactivos: bool = False,
    db: Session = Depends(get_db),
):
    """Obtener todos los detalles de compra con paginación."""
    try:
        detalle_crud = DetalleCompraCRUD(db)
        detalles = detalle_crud.obtener_detalles(
            skip=skip, limit=limit, incluir_inactivos=incluir_inactivos
        )
        return detalles
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener detalles de compra: {str(e)}",
        )


@router.get("/{detalle_id}", response_model=DetalleCompraResponse)
async def obtener_detalle(
    detalle_id: UUID,
    incluir_inactivos: bool = False,
    db: Session = Depends(get_db),
):
    """Obtener un detalle de compra por ID."""
    try:
        detalle_crud = DetalleCompraCRUD(db)
        detalle = detalle_crud.obtener_detalle(
            detalle_id, incluir_inactivos=incluir_inactivos
        )
        if not detalle:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Detalle de compra no encontrado",
            )
        return detalle
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener detalle de compra: {str(e)}",
        )


@router.get("/compra/{id_compra}", response_model=List[DetalleCompraResponse])
async def obtener_detalles_por_compra(
    id_compra: UUID,
    skip: int = 0,
    limit: int = 100,
    incluir_inactivos: bool = False,
    db: Session = Depends(get_db),
):
    """Obtener detalles de compra por ID de compra."""
    try:
        detalle_crud = DetalleCompraCRUD(db)
        detalles = detalle_crud.obtener_detalles_por_compra(
            id_compra=id_compra,
            skip=skip,
            limit=limit,
            incluir_inactivos=incluir_inactivos,
        )
        return detalles
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener detalles por compra: {str(e)}",
        )


@router.get("/producto/{id_producto}", response_model=List[DetalleCompraResponse])
async def obtener_detalles_por_producto(
    id_producto: UUID,
    skip: int = 0,
    limit: int = 100,
    incluir_inactivos: bool = False,
    db: Session = Depends(get_db),
):
    """Obtener detalles de compra por ID de producto."""
    try:
        detalle_crud = DetalleCompraCRUD(db)
        detalles = detalle_crud.obtener_detalles_por_producto(
            id_producto=id_producto,
            skip=skip,
            limit=limit,
            incluir_inactivos=incluir_inactivos,
        )
        return detalles
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener detalles por producto: {str(e)}",
        )


@router.post(
    "/", response_model=DetalleCompraResponse, status_code=status.HTTP_201_CREATED
)
async def crear_detalle(
    detalle_data: DetalleCompraCreate, db: Session = Depends(get_db)
):
    """Crear un nuevo detalle de compra."""
    try:
        detalle_crud = DetalleCompraCRUD(db)
        detalle = detalle_crud.crear_detalle(
            id_producto=detalle_data.id_producto,
            id_compra=detalle_data.id_compra,
            cantidad=detalle_data.cantidad,
            subtotal=detalle_data.subtotal,
        )
        return detalle
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear detalle de compra: {str(e)}",
        )


@router.put("/{detalle_id}", response_model=DetalleCompraResponse)
async def actualizar_detalle(
    detalle_id: UUID,
    detalle_data: DetalleCompraUpdate,
    db: Session = Depends(get_db),
):
    """Actualizar un detalle de compra existente."""
    try:
        detalle_crud = DetalleCompraCRUD(db)

        detalle_existente = detalle_crud.obtener_detalle(
            detalle_id, incluir_inactivos=True
        )
        if not detalle_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Detalle de compra no encontrado",
            )

        campos_actualizacion = {
            k: v for k, v in detalle_data.dict().items() if v is not None
        }

        if not campos_actualizacion:
            return detalle_existente

        detalle_actualizado = detalle_crud.actualizar_detalle(
            detalle_id, **campos_actualizacion
        )
        return detalle_actualizado
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar detalle de compra: {str(e)}",
        )


@router.delete("/{detalle_id}", response_model=RespuestaAPI)
async def eliminar_detalle(detalle_id: UUID, db: Session = Depends(get_db)):
    """Desactivar un detalle de compra."""
    try:
        detalle_crud = DetalleCompraCRUD(db)

        detalle_existente = detalle_crud.obtener_detalle(
            detalle_id, incluir_inactivos=True
        )
        if not detalle_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Detalle de compra no encontrado",
            )

        eliminada = detalle_crud.eliminar_detalle(detalle_id)
        if eliminada:
            return RespuestaAPI(
                mensaje="Detalle de compra desactivado exitosamente",
                exito=True,
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El detalle de compra ya estaba inactivo",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al desactivar detalle de compra: {str(e)}",
        )


@router.put("/{detalle_id}/activar", response_model=RespuestaAPI)
async def activar_detalle(detalle_id: UUID, db: Session = Depends(get_db)):
    """Reactivar un detalle de compra."""
    try:
        detalle_crud = DetalleCompraCRUD(db)

        detalle_existente = detalle_crud.obtener_detalle(
            detalle_id, incluir_inactivos=True
        )
        if not detalle_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Detalle de compra no encontrado",
            )

        activada = detalle_crud.activar_detalle(detalle_id)
        if activada:
            return RespuestaAPI(
                mensaje="Detalle de compra activado exitosamente",
                exito=True,
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El detalle de compra ya estaba activo",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al activar detalle de compra: {str(e)}",
        )
