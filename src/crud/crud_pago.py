"""
Operaciones CRUD para Pago
"""

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from typing import List, Optional
from uuid import UUID

from entities.pago import Pago
from sqlalchemy.orm import Session

METODOS_VALIDOS = {"EFECTIVO", "TARJETA", "TRANSFERENCIA", "NEQUI", "DAVIPLATA"}


class PagoCRUD:
    def __init__(self, db: Session):
        self.db = db

    def crear_pago(
        self,
        metodo: str,
        monto: float,
        id_caja: UUID,
        id_compra: UUID,
    ) -> Pago:
        if not metodo or len(metodo.strip()) == 0:
            raise ValueError("El método de pago es obligatorio")

        metodo_upper = metodo.strip().upper()
        if metodo_upper not in METODOS_VALIDOS:
            raise ValueError(
                f"Método de pago no válido. Opciones: {', '.join(METODOS_VALIDOS)}"
            )

        if monto is None or monto <= 0:
            raise ValueError("El monto debe ser un valor positivo")

        if id_caja is None:
            raise ValueError("La caja registradora es obligatoria")

        if id_compra is None:
            raise ValueError("La compra es obligatoria")

        pago = Pago(
            metodo=metodo_upper,
            monto=monto,
            id_caja=id_caja,
            id_compra=id_compra,
            activo=True,
        )
        self.db.add(pago)
        self.db.commit()
        self.db.refresh(pago)
        return pago

    def obtener_pago(
        self, pago_id: UUID, incluir_inactivos: bool = False
    ) -> Optional[Pago]:
        query = self.db.query(Pago).filter(Pago.id == pago_id)
        if not incluir_inactivos:
            query = query.filter(Pago.activo.is_(True))
        return query.first()

    def obtener_pagos(
        self, skip: int = 0, limit: int = 100, incluir_inactivos: bool = False
    ) -> List[Pago]:
        query = self.db.query(Pago)
        if not incluir_inactivos:
            query = query.filter(Pago.activo.is_(True))
        return query.offset(skip).limit(limit).all()

    def obtener_pagos_por_compra(
        self,
        id_compra: UUID,
        skip: int = 0,
        limit: int = 100,
        incluir_inactivos: bool = False,
    ) -> List[Pago]:
        query = self.db.query(Pago).filter(Pago.id_compra == id_compra)
        if not incluir_inactivos:
            query = query.filter(Pago.activo.is_(True))
        return query.offset(skip).limit(limit).all()

    def obtener_pagos_por_caja(
        self,
        id_caja: UUID,
        skip: int = 0,
        limit: int = 100,
        incluir_inactivos: bool = False,
    ) -> List[Pago]:
        query = self.db.query(Pago).filter(Pago.id_caja == id_caja)
        if not incluir_inactivos:
            query = query.filter(Pago.activo.is_(True))
        return query.offset(skip).limit(limit).all()

    def actualizar_pago(self, pago_id: UUID, **kwargs) -> Optional[Pago]:
        pago = self.obtener_pago(pago_id, incluir_inactivos=True)
        if not pago:
            return None

        if "metodo" in kwargs:
            metodo = kwargs["metodo"]
            if not metodo or len(metodo.strip()) == 0:
                raise ValueError("El método de pago es obligatorio")
            metodo_upper = metodo.strip().upper()
            if metodo_upper not in METODOS_VALIDOS:
                raise ValueError(
                    f"Método de pago no válido. Opciones: {', '.join(METODOS_VALIDOS)}"
                )
            kwargs["metodo"] = metodo_upper

        if "monto" in kwargs:
            if kwargs["monto"] is None or kwargs["monto"] <= 0:
                raise ValueError("El monto debe ser un valor positivo")

        for key, value in kwargs.items():
            if hasattr(pago, key):
                setattr(pago, key, value)

        self.db.commit()
        self.db.refresh(pago)
        return pago

    def eliminar_pago(self, pago_id: UUID) -> bool:
        pago = self.obtener_pago(pago_id, incluir_inactivos=True)
        if pago and pago.activo:
            pago.activo = False
            self.db.commit()
            return True
        return False

    def activar_pago(self, pago_id: UUID) -> bool:
        pago = self.obtener_pago(pago_id, incluir_inactivos=True)
        if pago and not pago.activo:
            pago.activo = True
            self.db.commit()
            return True
        return False
