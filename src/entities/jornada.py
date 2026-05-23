import sys
import os
import uuid

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database.config import Base
from sqlalchemy import Column, DateTime, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Jornada(Base):
    __tablename__ = "jornadas"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    id_empleado = Column(UUID(as_uuid=True), ForeignKey("empleados.id"), nullable=False)
    id_caja = Column(
        UUID(as_uuid=True), ForeignKey("cajas_registradoras.id"), nullable=False
    )
    inicio_jornada = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    fin_jornada = Column(DateTime(timezone=True), nullable=True)
    activo = Column(Boolean, nullable=False, default=True)  # ← AGREGADO

    empleado = relationship("Empleado")
    caja = relationship("CajaRegistradora")

    def __repr__(self):
        return f"<​Jornada(id={self.id}, inicio={self.inicio_jornada}, fin={self.fin_jornada}, activo={self.activo})>"
