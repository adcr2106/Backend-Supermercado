"""
Operaciones CRUD para Categoria
"""

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from typing import List, Optional
from uuid import UUID

from entities.categoria import Categoria
from sqlalchemy.orm import Session


class CategoriaCRUD:
    def __init__(self, db: Session):
        self.db = db

    def crear_categoria(self, nombre: str) -> Categoria:
        if not nombre or len(nombre.strip()) == 0:
            raise ValueError("El nombre de la categoría es obligatorio")

        if len(nombre) > 100:
            raise ValueError("El nombre no puede exceder 100 caracteres")

        if self.obtener_categoria_por_nombre(nombre, incluir_inactivos=True):
            raise ValueError("Ya existe una categoría con ese nombre")

        categoria = Categoria(nombre=nombre.strip(), activo=True)
        self.db.add(categoria)
        self.db.commit()
        self.db.refresh(categoria)
        return categoria

    def obtener_categoria(
        self, categoria_id: UUID, incluir_inactivos: bool = False
    ) -> Optional[Categoria]:
        query = self.db.query(Categoria).filter(Categoria.id_categoria == categoria_id)
        if not incluir_inactivos:
            query = query.filter(Categoria.activo.is_(True))
        return query.first()

    def obtener_categoria_por_nombre(
        self, nombre: str, incluir_inactivos: bool = False
    ) -> Optional[Categoria]:
        query = self.db.query(Categoria).filter(Categoria.nombre == nombre.strip())
        if not incluir_inactivos:
            query = query.filter(Categoria.activo.is_(True))
        return query.first()

    def obtener_categorias(
        self, skip: int = 0, limit: int = 100, incluir_inactivos: bool = False
    ) -> List[Categoria]:
        query = self.db.query(Categoria)
        if not incluir_inactivos:
            query = query.filter(Categoria.activo.is_(True))
        return query.offset(skip).limit(limit).all()

    def actualizar_categoria(self, categoria_id: UUID, **kwargs) -> Optional[Categoria]:
        categoria = self.obtener_categoria(categoria_id, incluir_inactivos=True)
        if not categoria:
            return None

        if "nombre" in kwargs:
            nombre = kwargs["nombre"]

            if not nombre or len(nombre.strip()) == 0:
                raise ValueError("El nombre es obligatorio")

            if len(nombre) > 100:
                raise ValueError("El nombre no puede exceder 100 caracteres")

            existente = self.obtener_categoria_por_nombre(
                nombre, incluir_inactivos=True
            )
            if existente and existente.id_categoria != categoria_id:
                raise ValueError("Ya existe una categoría con ese nombre")

            kwargs["nombre"] = nombre.strip()

        for key, value in kwargs.items():
            if hasattr(categoria, key):
                setattr(categoria, key, value)

        self.db.commit()
        self.db.refresh(categoria)
        return categoria

    def eliminar_categoria(self, categoria_id: UUID) -> bool:
        categoria = self.obtener_categoria(categoria_id, incluir_inactivos=True)
        if categoria and categoria.activo:
            categoria.activo = False
            self.db.commit()
            return True
        return False

    def activar_categoria(self, categoria_id: UUID) -> bool:
        categoria = self.obtener_categoria(categoria_id, incluir_inactivos=True)
        if categoria and not categoria.activo:
            categoria.activo = True
            self.db.commit()
            return True
        return False
