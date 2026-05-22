"""
Operaciones CRUD para Compra
"""

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from typing import List, Optional

from uuid import UUID

from entities.compra import Compra

from sqlalchemy.orm import Session


class CompraCRUD:

    def __init__(self, db: Session):

        self.db = db

    # =========================
    # CREAR
    # =========================

    def crear_compra(
        self,
        total: float,
        doc_cliente: str,
        doc_empleado: str,
    ) -> Compra:

        if not doc_cliente or len(doc_cliente.strip()) == 0:
            raise ValueError("El documento del cliente es obligatorio")

        if not doc_empleado or len(doc_empleado.strip()) == 0:
            raise ValueError("El documento del empleado es obligatorio")

        compra = Compra(
            total=total,
            doc_cliente=doc_cliente.strip(),
            doc_empleado=doc_empleado.strip(),
            activo=True,
        )

        self.db.add(compra)

        self.db.commit()

        self.db.refresh(compra)

        return compra

    # =========================
    # OBTENER POR ID
    # =========================

    def obtener_compra(
        self, compra_id: UUID, incluir_inactivos: bool = False
    ) -> Optional[Compra]:

        query = self.db.query(Compra).filter(Compra.id == compra_id)

        if not incluir_inactivos:

            query = query.filter(Compra.activo.is_(True))

        return query.first()

    # =========================
    # OBTENER TODOS
    # =========================

    def obtener_compras(
        self, skip: int = 0, limit: int = 100, incluir_inactivos: bool = False
    ) -> List[Compra]:

        query = self.db.query(Compra)

        if not incluir_inactivos:

            query = query.filter(Compra.activo.is_(True))

        return query.offset(skip).limit(limit).all()

    # =========================
    # OBTENER POR CLIENTE
    # =========================

    def obtener_compras_por_cliente(
        self,
        doc_cliente: str,
        skip: int = 0,
        limit: int = 100,
        incluir_inactivos: bool = False,
    ) -> List[Compra]:

        query = self.db.query(Compra).filter(Compra.doc_cliente == doc_cliente.strip())

        if not incluir_inactivos:

            query = query.filter(Compra.activo.is_(True))

        return query.offset(skip).limit(limit).all()

    # =========================
    # OBTENER POR EMPLEADO
    # =========================

    def obtener_compras_por_empleado(
        self,
        doc_empleado: str,
        skip: int = 0,
        limit: int = 100,
        incluir_inactivos: bool = False,
    ) -> List[Compra]:

        query = self.db.query(Compra).filter(
            Compra.doc_empleado == doc_empleado.strip()
        )

        if not incluir_inactivos:

            query = query.filter(Compra.activo.is_(True))

        return query.offset(skip).limit(limit).all()

    # =========================
    # ACTUALIZAR
    # =========================

    def actualizar_compra(self, compra_id: UUID, **kwargs) -> Optional[Compra]:

        compra = self.obtener_compra(compra_id, incluir_inactivos=True)

        if not compra:

            return None

        if "total" in kwargs:

            if kwargs["total"] is None or kwargs["total"] < 0:

                raise ValueError("El total debe ser un valor mayor o igual a 0")

        if "doc_cliente" in kwargs:

            doc_cliente = kwargs["doc_cliente"]

            if not doc_cliente or len(doc_cliente.strip()) == 0:

                raise ValueError("El documento del cliente es obligatorio")

            kwargs["doc_cliente"] = doc_cliente.strip()

        if "doc_empleado" in kwargs:

            doc_empleado = kwargs["doc_empleado"]

            if not doc_empleado or len(doc_empleado.strip()) == 0:

                raise ValueError("El documento del empleado es obligatorio")

            kwargs["doc_empleado"] = doc_empleado.strip()

        for key, value in kwargs.items():

            if hasattr(compra, key):

                setattr(compra, key, value)

        self.db.commit()

        self.db.refresh(compra)

        return compra

    # =========================
    # ELIMINAR
    # =========================

    def eliminar_compra(self, compra_id: UUID) -> bool:

        compra = self.obtener_compra(compra_id, incluir_inactivos=True)

        if compra and compra.activo:

            compra.activo = False

            self.db.commit()

            return True

        return False

    # =========================
    # ACTIVAR
    # =========================

    def activar_compra(self, compra_id: UUID) -> bool:

        compra = self.obtener_compra(compra_id, incluir_inactivos=True)

        if compra and not compra.activo:

            compra.activo = True

            self.db.commit()

            return True

        return False
