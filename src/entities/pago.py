import sys
import os
import uuid

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database.config import Base
from sqlalchemy import Column, String, Numeric, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, validates


class Pago(Base):
    __tablename__ = "pagos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    metodo = Column(String(50), nullable=False)
    monto = Column(Numeric(10, 2), nullable=False)
    activo = Column(Boolean, nullable=False, default=True)

    id_caja = Column(
        UUID(as_uuid=True), ForeignKey("cajas_registradoras.id"), nullable=False
    )
    id_compra = Column(UUID(as_uuid=True), ForeignKey("compras.id"), nullable=False)

    caja = relationship("CajaRegistradora")
    compra = relationship("Compra")

    @validates("metodo")
    def convert_mayus(self, key, value):
        return value.upper()

    def __repr__(self):
        return (
            f"<​Pago(metodo='{self.metodo}', monto={self.monto}, activo={self.activo})>"
        )
