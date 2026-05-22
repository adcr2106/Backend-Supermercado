"""
Operaciones CRUD para DetalleCompra
"""

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from typing import List, Optional
from uuid import UUID

from entities.detalle_compra import DetalleCompra
from sqlalchemy.orm import Session


class DetalleCompraCRUD:
    def __init__(self, db: Session):
        self.db = db

    def crear_detalle(
        self,
        id_producto: UUID,
        id_compra: UUID,
        cantidad: int,
        subtotal: float,
    ) -> DetalleCompra:
        if id_producto is None:
            raise ValueError("El producto es obligatorio")

        if id_compra is None:
            raise ValueError("La compra es obligatoria")

        if cantidad is None or cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a cero")

        if subtotal is None or subtotal < 0:
            raise ValueError("El subtotal debe ser un valor positivo")

        detalle = DetalleCompra(
            id_producto=id_producto,
            id_compra=id_compra,
            cantidad=cantidad,
            subtotal=subtotal,
            activo=True,
        )
        self.db.add(detalle)
        self.db.commit()
        self.db.refresh(detalle)
        return detalle

    def obtener_detalle(
        self, detalle_id: UUID, incluir_inactivos: bool = False
    ) -> Optional[DetalleCompra]:
        query = self.db.query(DetalleCompra).filter(
            DetalleCompra.id_detalle == detalle_id
        )
        if not incluir_inactivos:
            query = query.filter(DetalleCompra.activo.is_(True))
        return query.first()

    def obtener_detalles(
        self, skip: int = 0, limit: int = 100, incluir_inactivos: bool = False
    ) -> List[DetalleCompra]:
        query = self.db.query(DetalleCompra)
        if not incluir_inactivos:
            query = query.filter(DetalleCompra.activo.is_(True))
        return query.offset(skip).limit(limit).all()

    def obtener_detalles_por_compra(
        self,
        id_compra: UUID,
        skip: int = 0,
        limit: int = 100,
        incluir_inactivos: bool = False,
    ) -> List[DetalleCompra]:
        query = self.db.query(DetalleCompra).filter(
            DetalleCompra.id_compra == id_compra
        )
        if not incluir_inactivos:
            query = query.filter(DetalleCompra.activo.is_(True))
        return query.offset(skip).limit(limit).all()

    def obtener_detalles_por_producto(
        self,
        id_producto: UUID,
        skip: int = 0,
        limit: int = 100,
        incluir_inactivos: bool = False,
    ) -> List[DetalleCompra]:
        query = self.db.query(DetalleCompra).filter(
            DetalleCompra.id_producto == id_producto
        )
        if not incluir_inactivos:
            query = query.filter(DetalleCompra.activo.is_(True))
        return query.offset(skip).limit(limit).all()

    def actualizar_detalle(self, detalle_id: UUID, **kwargs) -> Optional[DetalleCompra]:
        detalle = self.obtener_detalle(detalle_id, incluir_inactivos=True)
        if not detalle:
            return None

        if "cantidad" in kwargs:
            if kwargs["cantidad"] is None or kwargs["cantidad"] <= 0:
                raise ValueError("La cantidad debe ser mayor a cero")

        if "subtotal" in kwargs:
            if kwargs["subtotal"] is None or kwargs["subtotal"] < 0:
                raise ValueError("El subtotal debe ser un valor positivo")

        for key, value in kwargs.items():
            if hasattr(detalle, key):
                setattr(detalle, key, value)

        self.db.commit()
        self.db.refresh(detalle)
        return detalle

    def eliminar_detalle(self, detalle_id: UUID) -> bool:
        detalle = self.obtener_detalle(detalle_id)
        if detalle:
            detalle.activo = False  # Eliminación lógica
            self.db.commit()
            return True
        return False

    # Añadir activar_detalle:
    def activar_detalle(self, detalle_id: UUID) -> bool:
        detalle = (
            self.db.query(DetalleCompra)
            .filter(DetalleCompra.id_detalle == detalle_id)
            .first()
        )
        if detalle:
            detalle.activo = True
            self.db.commit()
            return True
        return False
