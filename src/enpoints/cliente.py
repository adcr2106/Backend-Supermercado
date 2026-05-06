"""
API de Clientes - Endpoints para gestión de clientes
"""

from typing import List
from uuid import UUID
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from crud.crud_cliente import ClienteCRUD
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from schemas.cliente import ClienteCreate, ClienteResponse, ClienteUpdate, RespuestaAPI
from sqlalchemy.orm import Session

router = APIRouter(prefix="/clientes", tags=["clientes"])


@router.get("/", response_model=List[ClienteResponse])
async def obtener_clientes(
    skip: int = 0,
    limit: int = 100,
    incluir_inactivos: bool = False,
    db: Session = Depends(get_db),
):
    """Obtener todos los clientes con paginación."""
    try:
        cliente_crud = ClienteCRUD(db)
        clientes = cliente_crud.obtener_clientes(
            skip=skip, limit=limit, incluir_inactivos=incluir_inactivos
        )
        return clientes
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener clientes: {str(e)}",
        )


@router.get("/{cliente_id}", response_model=ClienteResponse)
async def obtener_cliente(
    cliente_id: UUID,
    incluir_inactivos: bool = False,
    db: Session = Depends(get_db),
):
    """Obtener un cliente por ID."""
    try:
        cliente_crud = ClienteCRUD(db)
        cliente = cliente_crud.obtener_cliente(
            cliente_id, incluir_inactivos=incluir_inactivos
        )
        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente no encontrado",
            )
        return cliente
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener cliente: {str(e)}",
        )


@router.get("/documento/{documento}", response_model=ClienteResponse)
async def obtener_cliente_por_documento(documento: str, db: Session = Depends(get_db)):
    """Obtener un cliente por documento."""
    try:
        cliente_crud = ClienteCRUD(db)
        cliente = cliente_crud.obtener_cliente_por_documento(documento)
        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente no encontrado",
            )
        return cliente
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener cliente: {str(e)}",
        )


@router.get("/correo/{correo}", response_model=ClienteResponse)
async def obtener_cliente_por_correo(correo: str, db: Session = Depends(get_db)):
    """Obtener un cliente por correo."""
    try:
        cliente_crud = ClienteCRUD(db)
        cliente = cliente_crud.obtener_cliente_por_correo(correo)
        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente no encontrado",
            )
        return cliente
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener cliente: {str(e)}",
        )


@router.post("/", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED)
async def crear_cliente(cliente_data: ClienteCreate, db: Session = Depends(get_db)):
    """Crear un nuevo cliente."""
    try:
        cliente_crud = ClienteCRUD(db)
        cliente = cliente_crud.crear_cliente(
            documento=cliente_data.documento,
            nombre=cliente_data.nombre,
            telefono=cliente_data.telefono,
            correo=cliente_data.correo,
        )
        return cliente
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear cliente: {str(e)}",
        )


@router.put("/{cliente_id}", response_model=ClienteResponse)
async def actualizar_cliente(
    cliente_id: UUID,
    cliente_data: ClienteUpdate,
    db: Session = Depends(get_db),
):
    """Actualizar un cliente existente."""
    try:
        cliente_crud = ClienteCRUD(db)

        cliente_existente = cliente_crud.obtener_cliente(
            cliente_id, incluir_inactivos=True
        )
        if not cliente_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente no encontrado",
            )

        campos_actualizacion = {
            k: v for k, v in cliente_data.dict().items() if v is not None
        }

        if not campos_actualizacion:
            return cliente_existente

        cliente_actualizado = cliente_crud.actualizar_cliente(
            cliente_id, **campos_actualizacion
        )
        return cliente_actualizado
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar cliente: {str(e)}",
        )


@router.delete("/{cliente_id}", response_model=RespuestaAPI)
async def eliminar_cliente(cliente_id: UUID, db: Session = Depends(get_db)):
    """Desactivar un cliente."""
    try:
        cliente_crud = ClienteCRUD(db)

        cliente_existente = cliente_crud.obtener_cliente(
            cliente_id, incluir_inactivos=True
        )
        if not cliente_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente no encontrado",
            )

        eliminada = cliente_crud.eliminar_cliente(cliente_id)
        if eliminada:
            return RespuestaAPI(
                mensaje="Cliente desactivado exitosamente",
                exito=True,
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El cliente ya estaba inactivo",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al desactivar cliente: {str(e)}",
        )


@router.put("/{cliente_id}/activar", response_model=RespuestaAPI)
async def activar_cliente(cliente_id: UUID, db: Session = Depends(get_db)):
    """Reactivar un cliente."""
    try:
        cliente_crud = ClienteCRUD(db)

        cliente_existente = cliente_crud.obtener_cliente(
            cliente_id, incluir_inactivos=True
        )
        if not cliente_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente no encontrado",
            )

        activada = cliente_crud.activar_cliente(cliente_id)
        if activada:
            return RespuestaAPI(
                mensaje="Cliente activado exitosamente",
                exito=True,
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El cliente ya estaba activo",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al activar cliente: {str(e)}",
        )
