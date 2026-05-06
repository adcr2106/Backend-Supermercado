import sys
import os
import uuid

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database.config import Base
from sqlalchemy import Column, Integer, Numeric, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class DetalleCompra(Base):
    __tablename__ = "detalle_compras"

    id_detalle = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    id_producto = Column(
        UUID(as_uuid=True), ForeignKey("productos.id_producto"), nullable=False
    )
    id_compra = Column(UUID(as_uuid=True), ForeignKey("compras.id"), nullable=False)

    cantidad = Column(Integer, nullable=False)
    subtotal = Column(Numeric(10, 2), nullable=False)
    activo = Column(Boolean, nullable=False, default=True)  # ← AGREGADO

    compra = relationship("Compra", back_populates="detalles")
    producto = relationship("Producto", back_populates="detalles")

    def __repr__(self):
        return f"<​DetalleCompra(cantidad={self.cantidad}, subtotal={self.subtotal}, activo={self.activo})>"
