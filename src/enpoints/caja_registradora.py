"""
API de CajaRegistradora - Endpoints para gestión de cajas registradoras
"""

from typing import List
from uuid import UUID
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from crud.crud_caja_registradora import CajaRegistradoraCRUD
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from schemas.caja_registradora import CajaRegistradoraResponse, RespuestaAPI
from sqlalchemy.orm import Session

router = APIRouter(prefix="/cajas-registradoras", tags=["cajas_registradoras"])


@router.get("/", response_model=List[CajaRegistradoraResponse])
async def obtener_cajas(
    skip: int = 0,
    limit: int = 100,
    incluir_inactivos: bool = False,
    db: Session = Depends(get_db),
):
    """Obtener todas las cajas registradoras con paginación."""
    try:
        caja_crud = CajaRegistradoraCRUD(db)
        cajas = caja_crud.obtener_cajas(
            skip=skip, limit=limit, incluir_inactivos=incluir_inactivos
        )
        return cajas
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener cajas registradoras: {str(e)}",
        )


@router.get("/{caja_id}", response_model=CajaRegistradoraResponse)
async def obtener_caja(
    caja_id: UUID,
    incluir_inactivos: bool = False,
    db: Session = Depends(get_db),
):
    """Obtener una caja registradora por ID."""
    try:
        caja_crud = CajaRegistradoraCRUD(db)
        caja = caja_crud.obtener_caja(caja_id, incluir_inactivos=incluir_inactivos)
        if not caja:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Caja registradora no encontrada",
            )
        return caja
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener caja registradora: {str(e)}",
        )


@router.post(
    "/", response_model=CajaRegistradoraResponse, status_code=status.HTTP_201_CREATED
)
async def crear_caja(db: Session = Depends(get_db)):
    """Crear una nueva caja registradora."""
    try:
        caja_crud = CajaRegistradoraCRUD(db)
        caja = caja_crud.crear_caja()
        return caja
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear caja registradora: {str(e)}",
        )


@router.delete("/{caja_id}", response_model=RespuestaAPI)
async def eliminar_caja(caja_id: UUID, db: Session = Depends(get_db)):
    """Desactivar una caja registradora."""
    try:
        caja_crud = CajaRegistradoraCRUD(db)

        caja_existente = caja_crud.obtener_caja(caja_id, incluir_inactivos=True)
        if not caja_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Caja registradora no encontrada",
            )

        eliminada = caja_crud.eliminar_caja(caja_id)
        if eliminada:
            return RespuestaAPI(
                mensaje="Caja registradora desactivada exitosamente",
                exito=True,
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La caja registradora ya estaba inactiva",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al desactivar caja registradora: {str(e)}",
        )


@router.put("/{caja_id}/activar", response_model=RespuestaAPI)
async def activar_caja(caja_id: UUID, db: Session = Depends(get_db)):
    """Reactivar una caja registradora."""
    try:
        caja_crud = CajaRegistradoraCRUD(db)

        caja_existente = caja_crud.obtener_caja(caja_id, incluir_inactivos=True)
        if not caja_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Caja registradora no encontrada",
            )

        activada = caja_crud.activar_caja(caja_id)
        if activada:
            return RespuestaAPI(
                mensaje="Caja registradora activada exitosamente",
                exito=True,
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La caja registradora ya estaba activa",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al activar caja registradora: {str(e)}",
        )
