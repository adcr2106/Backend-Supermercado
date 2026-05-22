"""
API de Jornadas - Endpoints para gestión de jornadas
"""

from typing import List
from uuid import UUID
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from crud.crud_jornada import JornadaCRUD
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from schemas.jornada import JornadaCreate, JornadaResponse, JornadaUpdate, RespuestaAPI
from sqlalchemy.orm import Session

router = APIRouter(prefix="/jornadas", tags=["jornadas"])


@router.get("/", response_model=List[JornadaResponse])
async def obtener_jornadas(
    skip: int = 0,
    limit: int = 100,
    incluir_inactivos: bool = False,
    db: Session = Depends(get_db),
):
    """Obtener todas las jornadas con paginación."""
    try:
        jornada_crud = JornadaCRUD(db)
        jornadas = jornada_crud.obtener_jornadas(
            skip=skip, limit=limit, incluir_inactivos=incluir_inactivos
        )
        return jornadas
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener jornadas: {str(e)}",
        )


@router.get("/{jornada_id}", response_model=JornadaResponse)
async def obtener_jornada(
    jornada_id: UUID,
    incluir_inactivos: bool = False,
    db: Session = Depends(get_db),
):
    """Obtener una jornada por ID."""
    try:
        jornada_crud = JornadaCRUD(db)
        jornada = jornada_crud.obtener_jornada(
            jornada_id, incluir_inactivos=incluir_inactivos
        )
        if not jornada:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Jornada no encontrada",
            )
        return jornada
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener jornada: {str(e)}",
        )


@router.get("/empleado/{id_empleado}", response_model=List[JornadaResponse])
async def obtener_jornadas_por_empleado(
    id_empleado: UUID,
    skip: int = 0,
    limit: int = 100,
    incluir_inactivos: bool = False,
    db: Session = Depends(get_db),
):
    """Obtener jornadas por empleado."""
    try:
        jornada_crud = JornadaCRUD(db)
        jornadas = jornada_crud.obtener_jornadas_por_empleado(
            id_empleado=id_empleado,
            skip=skip,
            limit=limit,
            incluir_inactivos=incluir_inactivos,
        )
        return jornadas
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener jornadas por empleado: {str(e)}",
        )


@router.post("/", response_model=JornadaResponse, status_code=status.HTTP_201_CREATED)
async def crear_jornada(jornada_data: JornadaCreate, db: Session = Depends(get_db)):
    """Crear una nueva jornada."""
    try:
        jornada_crud = JornadaCRUD(db)
        jornada = jornada_crud.crear_jornada(
            id_empleado=jornada_data.id_empleado,
            id_caja=jornada_data.id_caja,
        )
        return jornada
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear jornada: {str(e)}",
        )


@router.put("/{jornada_id}", response_model=JornadaResponse)
async def actualizar_jornada(
    jornada_id: UUID,
    jornada_data: JornadaUpdate,
    db: Session = Depends(get_db),
):
    """Actualizar una jornada existente."""
    try:
        jornada_crud = JornadaCRUD(db)

        jornada_existente = jornada_crud.obtener_jornada(
            jornada_id, incluir_inactivos=True
        )
        if not jornada_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Jornada no encontrada",
            )

        campos_actualizacion = {
            k: v for k, v in jornada_data.dict().items() if v is not None
        }

        if not campos_actualizacion:
            return jornada_existente

        jornada_actualizada = jornada_crud.actualizar_jornada(
            jornada_id, **campos_actualizacion
        )
        return jornada_actualizada
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar jornada: {str(e)}",
        )


@router.put("/{jornada_id}/cerrar", response_model=JornadaResponse)
async def cerrar_jornada(jornada_id: UUID, db: Session = Depends(get_db)):
    """Cerrar una jornada."""
    try:
        jornada_crud = JornadaCRUD(db)

        jornada_existente = jornada_crud.obtener_jornada(
            jornada_id, incluir_inactivos=True
        )
        if not jornada_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Jornada no encontrada",
            )

        jornada_cerrada = jornada_crud.cerrar_jornada(jornada_id)
        if not jornada_cerrada:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se pudo cerrar la jornada",
            )
        return jornada_cerrada
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al cerrar jornada: {str(e)}",
        )


@router.delete("/{jornada_id}", response_model=RespuestaAPI)
async def eliminar_jornada(jornada_id: UUID, db: Session = Depends(get_db)):
    """Desactivar una jornada."""
    try:
        jornada_crud = JornadaCRUD(db)

        jornada_existente = jornada_crud.obtener_jornada(
            jornada_id, incluir_inactivos=True
        )
        if not jornada_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Jornada no encontrada",
            )

        eliminada = jornada_crud.eliminar_jornada(jornada_id)
        if eliminada:
            return RespuestaAPI(
                mensaje="Jornada desactivada exitosamente",
                exito=True,
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La jornada ya estaba inactiva",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al desactivar jornada: {str(e)}",
        )


@router.put("/{jornada_id}/activar", response_model=RespuestaAPI)
async def activar_jornada(jornada_id: UUID, db: Session = Depends(get_db)):
    """Reactivar una jornada."""
    try:
        jornada_crud = JornadaCRUD(db)

        jornada_existente = jornada_crud.obtener_jornada(
            jornada_id, incluir_inactivos=True
        )
        if not jornada_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Jornada no encontrada",
            )

        activada = jornada_crud.activar_jornada(jornada_id)
        if activada:
            return RespuestaAPI(
                mensaje="Jornada activada exitosamente",
                exito=True,
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La jornada ya estaba activa",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al activar jornada: {str(e)}",
        )
