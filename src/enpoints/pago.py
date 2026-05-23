"""
API de Pagos - Endpoints para gestión de pagos
"""

from typing import List
from uuid import UUID
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from crud.crud_pago import PagoCRUD
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from schemas.pago import PagoCreate, PagoResponse, PagoUpdate, RespuestaAPI
from sqlalchemy.orm import Session

router = APIRouter(prefix="/pagos", tags=["pagos"])


@router.get("/", response_model=List[PagoResponse])
async def obtener_pagos(
    skip: int = 0,
    limit: int = 100,
    incluir_inactivos: bool = False,
    db: Session = Depends(get_db),
):
    """Obtener todos los pagos con paginación."""
    try:
        pago_crud = PagoCRUD(db)
        pagos = pago_crud.obtener_pagos(
            skip=skip, limit=limit, incluir_inactivos=incluir_inactivos
        )
        return pagos
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener pagos: {str(e)}",
        )


@router.get("/{pago_id}", response_model=PagoResponse)
async def obtener_pago(
    pago_id: UUID,
    incluir_inactivos: bool = False,
    db: Session = Depends(get_db),
):
    """Obtener un pago por ID."""
    try:
        pago_crud = PagoCRUD(db)
        pago = pago_crud.obtener_pago(pago_id, incluir_inactivos=incluir_inactivos)
        if not pago:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pago no encontrado",
            )
        return pago
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener pago: {str(e)}",
        )


@router.get("/compra/{id_compra}", response_model=List[PagoResponse])
async def obtener_pagos_por_compra(
    id_compra: UUID,
    skip: int = 0,
    limit: int = 100,
    incluir_inactivos: bool = False,
    db: Session = Depends(get_db),
):
    """Obtener pagos por ID de compra."""
    try:
        pago_crud = PagoCRUD(db)
        pagos = pago_crud.obtener_pagos_por_compra(
            id_compra=id_compra,
            skip=skip,
            limit=limit,
            incluir_inactivos=incluir_inactivos,
        )
        return pagos
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener pagos por compra: {str(e)}",
        )


@router.get("/caja/{id_caja}", response_model=List[PagoResponse])
async def obtener_pagos_por_caja(
    id_caja: UUID,
    skip: int = 0,
    limit: int = 100,
    incluir_inactivos: bool = False,
    db: Session = Depends(get_db),
):
    """Obtener pagos por ID de caja registradora."""
    try:
        pago_crud = PagoCRUD(db)
        pagos = pago_crud.obtener_pagos_por_caja(
            id_caja=id_caja,
            skip=skip,
            limit=limit,
            incluir_inactivos=incluir_inactivos,
        )
        return pagos
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener pagos por caja: {str(e)}",
        )


@router.post("/", response_model=PagoResponse, status_code=status.HTTP_201_CREATED)
async def crear_pago(pago_data: PagoCreate, db: Session = Depends(get_db)):
    """Crear un nuevo pago."""
    try:
        pago_crud = PagoCRUD(db)
        pago = pago_crud.crear_pago(
            metodo=pago_data.metodo,
            monto=pago_data.monto,
            id_caja=pago_data.id_caja,
            id_compra=pago_data.id_compra,
        )
        return pago
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear pago: {str(e)}",
        )


@router.put("/{pago_id}", response_model=PagoResponse)
async def actualizar_pago(
    pago_id: UUID,
    pago_data: PagoUpdate,
    db: Session = Depends(get_db),
):
    """Actualizar un pago existente."""
    try:
        pago_crud = PagoCRUD(db)

        pago_existente = pago_crud.obtener_pago(pago_id, incluir_inactivos=True)
        if not pago_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pago no encontrado",
            )

        campos_actualizacion = {
            k: v for k, v in pago_data.dict().items() if v is not None
        }

        if not campos_actualizacion:
            return pago_existente

        pago_actualizado = pago_crud.actualizar_pago(pago_id, **campos_actualizacion)
        return pago_actualizado
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar pago: {str(e)}",
        )


@router.delete("/{pago_id}", response_model=RespuestaAPI)
async def eliminar_pago(pago_id: UUID, db: Session = Depends(get_db)):
    """Desactivar un pago."""
    try:
        pago_crud = PagoCRUD(db)

        pago_existente = pago_crud.obtener_pago(pago_id, incluir_inactivos=True)
        if not pago_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pago no encontrado",
            )

        eliminada = pago_crud.eliminar_pago(pago_id)
        if eliminada:
            return RespuestaAPI(
                mensaje="Pago desactivado exitosamente",
                exito=True,
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El pago ya estaba inactivo",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al desactivar pago: {str(e)}",
        )


@router.put("/{pago_id}/activar", response_model=RespuestaAPI)
async def activar_pago(pago_id: UUID, db: Session = Depends(get_db)):
    """Reactivar un pago."""
    try:
        pago_crud = PagoCRUD(db)

        pago_existente = pago_crud.obtener_pago(pago_id, incluir_inactivos=True)
        if not pago_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pago no encontrado",
            )

        activada = pago_crud.activar_pago(pago_id)
        if activada:
            return RespuestaAPI(
                mensaje="Pago activado exitosamente",
                exito=True,
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El pago ya estaba activo",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al activar pago: {str(e)}",
        )
