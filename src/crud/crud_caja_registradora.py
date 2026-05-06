"""
Operaciones CRUD para CajaRegistradora
"""

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from typing import List, Optional
from uuid import UUID

from entities.caja_registradora import CajaRegistradora
from sqlalchemy.orm import Session


class CajaRegistradoraCRUD:
    def __init__(self, db: Session):
        self.db = db

    def crear_caja(self) -> CajaRegistradora:
        caja = CajaRegistradora(activo=True)
        self.db.add(caja)
        self.db.commit()
        self.db.refresh(caja)
        return caja

    def obtener_caja(
        self, caja_id: UUID, incluir_inactivos: bool = False
    ) -> Optional[CajaRegistradora]:
        query = self.db.query(CajaRegistradora).filter(CajaRegistradora.id == caja_id)
        if not incluir_inactivos:
            query = query.filter(CajaRegistradora.activo.is_(True))
        return query.first()

    def obtener_cajas(
        self, skip: int = 0, limit: int = 100, incluir_inactivos: bool = False
    ) -> List[CajaRegistradora]:
        query = self.db.query(CajaRegistradora)
        if not incluir_inactivos:
            query = query.filter(CajaRegistradora.activo.is_(True))
        return query.offset(skip).limit(limit).all()

    def eliminar_caja(self, caja_id: UUID) -> bool:
        caja = self.obtener_caja(caja_id, incluir_inactivos=True)
        if caja and caja.activo:
            caja.activo = False
            self.db.commit()
            return True
        return False

    def activar_caja(self, caja_id: UUID) -> bool:
        caja = self.obtener_caja(caja_id, incluir_inactivos=True)
        if caja and not caja.activo:
            caja.activo = True
            self.db.commit()
            return True
        return False
