import sys
import os
import uuid

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database.config import Base
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Compra(Base):
    __tablename__ = "compras"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    fecha_hora = Column(DateTime(timezone=True), server_default=func.now())
    total = Column(Numeric(10, 2), nullable=False)
    activo = Column(Boolean, nullable=False, default=True)

    doc_cliente = Column(String(50), ForeignKey("clientes.documento"), nullable=False)
    doc_empleado = Column(String(50), ForeignKey("empleados.documento"), nullable=False)

    cliente = relationship("Cliente")
    empleado = relationship("Empleado", back_populates="compras")
    detalles = relationship("DetalleCompra", back_populates="compra")

    def __repr__(self):
        return f"<​Compra(id={self.id}, total={self.total}, activo={self.activo})>"
