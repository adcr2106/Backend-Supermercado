"""
Operaciones CRUD para Jornada
"""

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from entities.jornada import Jornada
from sqlalchemy.orm import Session


class JornadaCRUD:
    def __init__(self, db: Session):
        self.db = db

    def crear_jornada(
        self,
        id_empleado: UUID,
        id_caja: UUID,
    ) -> Jornada:
        if id_empleado is None:
            raise ValueError("El empleado es obligatorio")

        if id_caja is None:
            raise ValueError("La caja registradora es obligatoria")

        jornada_activa = self.obtener_jornada_activa_por_empleado(id_empleado)
        if jornada_activa:
            raise ValueError("El empleado ya tiene una jornada activa abierta")

        jornada = Jornada(
            id_empleado=id_empleado,
            id_caja=id_caja,
            activo=True,
        )
        self.db.add(jornada)
        self.db.commit()
        self.db.refresh(jornada)
        return jornada

    def obtener_jornada(
        self, jornada_id: UUID, incluir_inactivos: bool = False
    ) -> Optional[Jornada]:
        query = self.db.query(Jornada).filter(Jornada.id == jornada_id)
        if not incluir_inactivos:
            query = query.filter(Jornada.activo.is_(True))
        return query.first()

    def obtener_jornadas(
        self, skip: int = 0, limit: int = 100, incluir_inactivos: bool = False
    ) -> List[Jornada]:
        query = self.db.query(Jornada)
        if not incluir_inactivos:
            query = query.filter(Jornada.activo.is_(True))
        return query.offset(skip).limit(limit).all()

    def obtener_jornadas_por_empleado(
        self,
        id_empleado: UUID,
        skip: int = 0,
        limit: int = 100,
        incluir_inactivos: bool = False,
    ) -> List[Jornada]:
        query = self.db.query(Jornada).filter(Jornada.id_empleado == id_empleado)
        if not incluir_inactivos:
            query = query.filter(Jornada.activo.is_(True))
        return query.offset(skip).limit(limit).all()

    def obtener_jornada_activa_por_empleado(
        self, id_empleado: UUID
    ) -> Optional[Jornada]:
        return (
            self.db.query(Jornada)
            .filter(
                Jornada.id_empleado == id_empleado,
                Jornada.fin_jornada.is_(None),
                Jornada.activo.is_(True),
            )
            .first()
        )

    def cerrar_jornada(self, jornada_id: UUID) -> Optional[Jornada]:
        jornada = self.obtener_jornada(jornada_id)
        if not jornada:
            return None

        if jornada.fin_jornada is not None:
            raise ValueError("La jornada ya fue cerrada anteriormente")

        jornada.fin_jornada = datetime.now()
        self.db.commit()
        self.db.refresh(jornada)
        return jornada

    def actualizar_jornada(self, jornada_id: UUID, **kwargs) -> Optional[Jornada]:
        jornada = self.obtener_jornada(jornada_id, incluir_inactivos=True)
        if not jornada:
            return None

        if "fin_jornada" in kwargs and kwargs["fin_jornada"] is not None:
            if (
                jornada.inicio_jornada
                and kwargs["fin_jornada"] < jornada.inicio_jornada
            ):
                raise ValueError("El fin de jornada no puede ser anterior al inicio")

        for key, value in kwargs.items():
            if hasattr(jornada, key):
                setattr(jornada, key, value)

        self.db.commit()
        self.db.refresh(jornada)
        return jornada

    def eliminar_jornada(self, jornada_id: UUID) -> bool:
        jornada = self.obtener_jornada(jornada_id, incluir_inactivos=True)
        if jornada and jornada.activo:
            jornada.activo = False
            self.db.commit()
            return True
        return False

    def activar_jornada(self, jornada_id: UUID) -> bool:
        jornada = self.obtener_jornada(jornada_id, incluir_inactivos=True)
        if jornada and not jornada.activo:
            jornada.activo = True
            self.db.commit()
            return True
        return False
