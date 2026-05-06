"""
Operaciones CRUD para Proveedor
"""

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from typing import List, Optional
from uuid import UUID

from entities.proveedor import Proveedor
from sqlalchemy.orm import Session


class ProveedorCRUD:
    def __init__(self, db: Session):
        self.db = db

    def crear_proveedor(self, nombre: str) -> Proveedor:
        if not nombre or len(nombre.strip()) == 0:
            raise ValueError("El nombre del proveedor es obligatorio")
        if len(nombre) > 100:
            raise ValueError("El nombre no puede exceder 100 caracteres")

        if self.obtener_proveedor_por_nombre(nombre, incluir_inactivos=True):
            raise ValueError("Ya existe un proveedor con ese nombre")

        proveedor = Proveedor(nombre=nombre.strip(), activo=True)
        self.db.add(proveedor)
        self.db.commit()
        self.db.refresh(proveedor)
        return proveedor

    def obtener_proveedor(
        self, proveedor_id: UUID, incluir_inactivos: bool = False
    ) -> Optional[Proveedor]:
        query = self.db.query(Proveedor).filter(Proveedor.id_proveedor == proveedor_id)
        if not incluir_inactivos:
            query = query.filter(Proveedor.activo.is_(True))
        return query.first()

    def obtener_proveedor_por_nombre(
        self, nombre: str, incluir_inactivos: bool = False
    ) -> Optional[Proveedor]:
        query = self.db.query(Proveedor).filter(Proveedor.nombre == nombre.strip())
        if not incluir_inactivos:
            query = query.filter(Proveedor.activo.is_(True))
        return query.first()

    def obtener_proveedores(
        self, skip: int = 0, limit: int = 100, incluir_inactivos: bool = False
    ) -> List[Proveedor]:
        query = self.db.query(Proveedor)
        if not incluir_inactivos:
            query = query.filter(Proveedor.activo.is_(True))
        return query.offset(skip).limit(limit).all()

    def actualizar_proveedor(self, proveedor_id: UUID, **kwargs) -> Optional[Proveedor]:
        proveedor = self.obtener_proveedor(proveedor_id, incluir_inactivos=True)
        if not proveedor:
            return None

        if "nombre" in kwargs:
            nombre = kwargs["nombre"]
            if not nombre or len(nombre.strip()) == 0:
                raise ValueError("El nombre del proveedor es obligatorio")
            if len(nombre) > 100:
                raise ValueError("El nombre no puede exceder 100 caracteres")
            existente = self.obtener_proveedor_por_nombre(
                nombre, incluir_inactivos=True
            )
            if existente and existente.id_proveedor != proveedor_id:
                raise ValueError("Ya existe un proveedor con ese nombre")
            kwargs["nombre"] = nombre.strip()

        for key, value in kwargs.items():
            if hasattr(proveedor, key):
                setattr(proveedor, key, value)

        self.db.commit()
        self.db.refresh(proveedor)
        return proveedor

    def eliminar_proveedor(self, proveedor_id: UUID) -> bool:
        proveedor = self.obtener_proveedor(proveedor_id, incluir_inactivos=True)
        if proveedor and proveedor.activo:
            proveedor.activo = False
            self.db.commit()
            return True
        return False

    def activar_proveedor(self, proveedor_id: UUID) -> bool:
        proveedor = self.obtener_proveedor(proveedor_id, incluir_inactivos=True)
        if proveedor and not proveedor.activo:
            proveedor.activo = True
            self.db.commit()
            return True
        return False
