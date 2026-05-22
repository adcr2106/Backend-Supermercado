"""
API de Productos - Endpoints para gestión de productos
"""

from typing import List
from uuid import UUID
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from crud.crud_producto import ProductoCRUD
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from schemas.producto import (
    ProductoCreate,
    ProductoResponse,
    ProductoUpdate,
    RespuestaAPI,
)
from sqlalchemy.orm import Session

router = APIRouter(prefix="/productos", tags=["productos"])


@router.get("/", response_model=List[ProductoResponse])
async def obtener_productos(
    skip: int = 0,
    limit: int = 100,
    incluir_inactivos: bool = False,
    db: Session = Depends(get_db),
):
    """Obtener todos los productos con paginación."""
    try:
        producto_crud = ProductoCRUD(db)
        productos = producto_crud.obtener_productos(
            skip=skip, limit=limit, incluir_inactivos=incluir_inactivos
        )
        return productos
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener productos: {str(e)}",
        )


@router.get("/{producto_id}", response_model=ProductoResponse)
async def obtener_producto(
    producto_id: UUID,
    incluir_inactivos: bool = False,
    db: Session = Depends(get_db),
):
    """Obtener un producto por ID."""
    try:
        producto_crud = ProductoCRUD(db)
        producto = producto_crud.obtener_producto(
            producto_id, incluir_inactivos=incluir_inactivos
        )
        if not producto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Producto no encontrado",
            )
        return producto
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener producto: {str(e)}",
        )


@router.get("/categoria/{id_categoria}", response_model=List[ProductoResponse])
async def obtener_productos_por_categoria(
    id_categoria: UUID,
    skip: int = 0,
    limit: int = 100,
    incluir_inactivos: bool = False,
    db: Session = Depends(get_db),
):
    """Obtener productos por categoría."""
    try:
        producto_crud = ProductoCRUD(db)
        productos = producto_crud.obtener_productos_por_categoria(
            id_categoria=id_categoria,
            skip=skip,
            limit=limit,
            incluir_inactivos=incluir_inactivos,
        )
        return productos
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener productos por categoría: {str(e)}",
        )


@router.get("/proveedor/{id_proveedor}", response_model=List[ProductoResponse])
async def obtener_productos_por_proveedor(
    id_proveedor: UUID,
    skip: int = 0,
    limit: int = 100,
    incluir_inactivos: bool = False,
    db: Session = Depends(get_db),
):
    """Obtener productos por proveedor."""
    try:
        producto_crud = ProductoCRUD(db)
        productos = producto_crud.obtener_productos_por_proveedor(
            id_proveedor=id_proveedor,
            skip=skip,
            limit=limit,
            incluir_inactivos=incluir_inactivos,
        )
        return productos
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener productos por proveedor: {str(e)}",
        )


@router.post("/", response_model=ProductoResponse, status_code=status.HTTP_201_CREATED)
async def crear_producto(producto_data: ProductoCreate, db: Session = Depends(get_db)):
    """Crear un nuevo producto."""
    try:
        producto_crud = ProductoCRUD(db)
        producto = producto_crud.crear_producto(
            nombre=producto_data.nombre,
            precio=producto_data.precio,
            stock=producto_data.stock,
            id_categoria=producto_data.id_categoria,
            id_proveedor=producto_data.id_proveedor,
        )
        return producto
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear producto: {str(e)}",
        )


@router.put("/{producto_id}", response_model=ProductoResponse)
async def actualizar_producto(
    producto_id: UUID,
    producto_data: ProductoUpdate,
    db: Session = Depends(get_db),
):
    """Actualizar un producto existente."""
    try:
        producto_crud = ProductoCRUD(db)

        producto_existente = producto_crud.obtener_producto(
            producto_id, incluir_inactivos=True
        )
        if not producto_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Producto no encontrado",
            )

        campos_actualizacion = {
            k: v for k, v in producto_data.dict().items() if v is not None
        }

        if not campos_actualizacion:
            return producto_existente

        producto_actualizado = producto_crud.actualizar_producto(
            producto_id, **campos_actualizacion
        )
        return producto_actualizado
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar producto: {str(e)}",
        )


@router.patch("/{producto_id}/stock", response_model=ProductoResponse)
async def actualizar_stock_producto(
    producto_id: UUID,
    stock: int,
    db: Session = Depends(get_db),
):
    """Actualizar únicamente el stock de un producto."""
    try:
        producto_crud = ProductoCRUD(db)

        producto_existente = producto_crud.obtener_producto(
            producto_id, incluir_inactivos=True
        )
        if not producto_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Producto no encontrado",
            )

        producto_actualizado = producto_crud.actualizar_stock(producto_id, stock)
        return producto_actualizado
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar stock del producto: {str(e)}",
        )


@router.delete("/{producto_id}", response_model=RespuestaAPI)
async def eliminar_producto(producto_id: UUID, db: Session = Depends(get_db)):
    """Desactivar un producto."""
    try:
        producto_crud = ProductoCRUD(db)

        producto_existente = producto_crud.obtener_producto(
            producto_id, incluir_inactivos=True
        )
        if not producto_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Producto no encontrado",
            )

        eliminada = producto_crud.eliminar_producto(producto_id)
        if eliminada:
            return RespuestaAPI(
                mensaje="Producto desactivado exitosamente",
                exito=True,
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El producto ya estaba inactivo",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al desactivar producto: {str(e)}",
        )


@router.put("/{producto_id}/activar", response_model=RespuestaAPI)
async def activar_producto(producto_id: UUID, db: Session = Depends(get_db)):
    """Reactivar un producto."""
    try:
        producto_crud = ProductoCRUD(db)

        producto_existente = producto_crud.obtener_producto(
            producto_id, incluir_inactivos=True
        )
        if not producto_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Producto no encontrado",
            )

        activada = producto_crud.activar_producto(producto_id)
        if activada:
            return RespuestaAPI(
                mensaje="Producto activado exitosamente",
                exito=True,
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El producto ya estaba activo",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al activar producto: {str(e)}",
        )
