"""
Operaciones CRUD para Producto
"""

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from typing import List, Optional
from uuid import UUID

from entities.producto import Producto
from sqlalchemy.orm import Session


class ProductoCRUD:
    def __init__(self, db: Session):
        self.db = db

    def crear_producto(
        self,
        nombre: str,
        precio: float,
        stock: int,
        id_categoria: UUID,
        id_proveedor: UUID,
    ) -> Producto:
        if not nombre or len(nombre.strip()) == 0:
            raise ValueError("El nombre del producto es obligatorio")
        if len(nombre) > 100:
            raise ValueError("El nombre no puede exceder 100 caracteres")

        if precio is None or precio < 0:
            raise ValueError("El precio debe ser un valor positivo")

        if stock is None or stock < 0:
            raise ValueError("El stock no puede ser negativo")

        if id_categoria is None:
            raise ValueError("La categoría es obligatoria")

        if id_proveedor is None:
            raise ValueError("El proveedor es obligatorio")

        producto = Producto(
            nombre=nombre.strip(),
            precio=precio,
            stock=stock,
            id_categoria=id_categoria,
            id_proveedor=id_proveedor,
            activo=True,
        )
        self.db.add(producto)
        self.db.commit()
        self.db.refresh(producto)
        return producto

    def obtener_producto(
        self, producto_id: UUID, incluir_inactivos: bool = False
    ) -> Optional[Producto]:
        query = self.db.query(Producto).filter(Producto.id_producto == producto_id)
        if not incluir_inactivos:
            query = query.filter(Producto.activo.is_(True))
        return query.first()

    def obtener_productos(
        self, skip: int = 0, limit: int = 100, incluir_inactivos: bool = False
    ) -> List[Producto]:
        query = self.db.query(Producto)
        if not incluir_inactivos:
            query = query.filter(Producto.activo.is_(True))
        return query.offset(skip).limit(limit).all()

    def obtener_productos_por_categoria(
        self,
        id_categoria: UUID,
        skip: int = 0,
        limit: int = 100,
        incluir_inactivos: bool = False,
    ) -> List[Producto]:
        query = self.db.query(Producto).filter(Producto.id_categoria == id_categoria)
        if not incluir_inactivos:
            query = query.filter(Producto.activo.is_(True))
        return query.offset(skip).limit(limit).all()

    def obtener_productos_por_proveedor(
        self,
        id_proveedor: UUID,
        skip: int = 0,
        limit: int = 100,
        incluir_inactivos: bool = False,
    ) -> List[Producto]:
        query = self.db.query(Producto).filter(Producto.id_proveedor == id_proveedor)
        if not incluir_inactivos:
            query = query.filter(Producto.activo.is_(True))
        return query.offset(skip).limit(limit).all()

    def actualizar_producto(self, producto_id: UUID, **kwargs) -> Optional[Producto]:
        producto = self.obtener_producto(producto_id, incluir_inactivos=True)
        if not producto:
            return None

        if "nombre" in kwargs:
            nombre = kwargs["nombre"]
            if not nombre or len(nombre.strip()) == 0:
                raise ValueError("El nombre del producto es obligatorio")
            if len(nombre) > 100:
                raise ValueError("El nombre no puede exceder 100 caracteres")
            kwargs["nombre"] = nombre.strip()

        if "precio" in kwargs:
            if kwargs["precio"] is None or kwargs["precio"] < 0:
                raise ValueError("El precio debe ser un valor positivo")

        if "stock" in kwargs:
            if kwargs["stock"] is None or kwargs["stock"] < 0:
                raise ValueError("El stock no puede ser negativo")

        for key, value in kwargs.items():
            if hasattr(producto, key):
                setattr(producto, key, value)

        self.db.commit()
        self.db.refresh(producto)
        return producto

    def actualizar_stock(self, producto_id: UUID, cantidad: int) -> Optional[Producto]:
        if cantidad < 0:
            raise ValueError("El stock no puede ser negativo")
        return self.actualizar_producto(producto_id, stock=cantidad)

    def eliminar_producto(self, producto_id: UUID) -> bool:
        producto = self.obtener_producto(producto_id, incluir_inactivos=True)
        if producto and producto.activo:
            producto.activo = False
            self.db.commit()
            return True
        return False

    def activar_producto(self, producto_id: UUID) -> bool:
        producto = self.obtener_producto(producto_id, incluir_inactivos=True)
        if producto and not producto.activo:
            producto.activo = True
            self.db.commit()
            return True
        return False
