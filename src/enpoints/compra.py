"""
API de Compras - Endpoints para gestión de compras
"""

from typing import List
from uuid import UUID
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from crud.crud_compra import CompraCRUD
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from schemas.compra import CompraCreate, CompraResponse, CompraUpdate, RespuestaAPI
from sqlalchemy.orm import Session

router = APIRouter(prefix="/compras", tags=["compras"])


@router.get("/", response_model=List[CompraResponse])
async def obtener_compras(
    skip: int = 0,
    limit: int = 100,
    incluir_inactivos: bool = False,
    db: Session = Depends(get_db),
):
    """Obtener todas las compras con paginación."""
    try:
        compra_crud = CompraCRUD(db)
        compras = compra_crud.obtener_compras(
            skip=skip, limit=limit, incluir_inactivos=incluir_inactivos
        )
        return compras
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener compras: {str(e)}",
        )


@router.get("/{compra_id}", response_model=CompraResponse)
async def obtener_compra(
    compra_id: UUID,
    incluir_inactivos: bool = False,
    db: Session = Depends(get_db),
):
    """Obtener una compra por ID."""
    try:
        compra_crud = CompraCRUD(db)
        compra = compra_crud.obtener_compra(
            compra_id, incluir_inactivos=incluir_inactivos
        )
        if not compra:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Compra no encontrada",
            )
        return compra
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener compra: {str(e)}",
        )


@router.get("/cliente/{doc_cliente}", response_model=List[CompraResponse])
async def obtener_compras_por_cliente(
    doc_cliente: str,
    skip: int = 0,
    limit: int = 100,
    incluir_inactivos: bool = False,
    db: Session = Depends(get_db),
):
    """Obtener compras por documento de cliente."""
    try:
        compra_crud = CompraCRUD(db)
        compras = compra_crud.obtener_compras_por_cliente(
            doc_cliente=doc_cliente,
            skip=skip,
            limit=limit,
            incluir_inactivos=incluir_inactivos,
        )
        return compras
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener compras por cliente: {str(e)}",
        )


@router.get("/empleado/{doc_empleado}", response_model=List[CompraResponse])
async def obtener_compras_por_empleado(
    doc_empleado: str,
    skip: int = 0,
    limit: int = 100,
    incluir_inactivos: bool = False,
    db: Session = Depends(get_db),
):
    """Obtener compras por documento de empleado."""
    try:
        compra_crud = CompraCRUD(db)
        compras = compra_crud.obtener_compras_por_empleado(
            doc_empleado=doc_empleado,
            skip=skip,
            limit=limit,
            incluir_inactivos=incluir_inactivos,
        )
        return compras
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener compras por empleado: {str(e)}",
        )


@router.post("/", response_model=CompraResponse, status_code=status.HTTP_201_CREATED)
async def crear_compra(compra_data: CompraCreate, db: Session = Depends(get_db)):
    """Crear una nueva compra."""
    try:
        compra_crud = CompraCRUD(db)
        compra = compra_crud.crear_compra(
            total=compra_data.total,
            doc_cliente=compra_data.doc_cliente,
            doc_empleado=compra_data.doc_empleado,
        )
        return compra
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear compra: {str(e)}",
        )


@router.put("/{compra_id}", response_model=CompraResponse)
async def actualizar_compra(
    compra_id: UUID,
    compra_data: CompraUpdate,
    db: Session = Depends(get_db),
):
    """Actualizar una compra existente."""
    try:
        compra_crud = CompraCRUD(db)

        compra_existente = compra_crud.obtener_compra(compra_id, incluir_inactivos=True)
        if not compra_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Compra no encontrada",
            )

        campos_actualizacion = {
            k: v for k, v in compra_data.dict().items() if v is not None
        }

        if not campos_actualizacion:
            return compra_existente

        compra_actualizada = compra_crud.actualizar_compra(
            compra_id, **campos_actualizacion
        )
        return compra_actualizada
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar compra: {str(e)}",
        )


@router.delete("/{compra_id}", response_model=RespuestaAPI)
async def eliminar_compra(compra_id: UUID, db: Session = Depends(get_db)):
    """Desactivar una compra."""
    try:
        compra_crud = CompraCRUD(db)

        compra_existente = compra_crud.obtener_compra(compra_id, incluir_inactivos=True)
        if not compra_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Compra no encontrada",
            )

        eliminada = compra_crud.eliminar_compra(compra_id)
        if eliminada:
            return RespuestaAPI(
                mensaje="Compra desactivada exitosamente",
                exito=True,
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La compra ya estaba inactiva",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al desactivar compra: {str(e)}",
        )


@router.put("/{compra_id}/activar", response_model=RespuestaAPI)
async def activar_compra(compra_id: UUID, db: Session = Depends(get_db)):
    """Reactivar una compra."""
    try:
        compra_crud = CompraCRUD(db)

        compra_existente = compra_crud.obtener_compra(compra_id, incluir_inactivos=True)
        if not compra_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Compra no encontrada",
            )

        activada = compra_crud.activar_compra(compra_id)
        if activada:
            return RespuestaAPI(
                mensaje="Compra activada exitosamente",
                exito=True,
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La compra ya estaba activa",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al activar compra: {str(e)}",
        )
