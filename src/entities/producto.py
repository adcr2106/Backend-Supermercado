import sys
import os
import uuid

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database.config import Base
from sqlalchemy import Column, String, Numeric, Integer, Boolean, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Producto(Base):
    __tablename__ = "productos"

    id_producto = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    nombre = Column(String(100), nullable=False)
    precio = Column(Numeric(10, 2), nullable=False)
    stock = Column(Integer, nullable=False)
    activo = Column(Boolean, nullable=False, default=True)

    id_categoria = Column(
        UUID(as_uuid=True), ForeignKey("categorias.id_categoria"), nullable=False
    )
    id_proveedor = Column(
        UUID(as_uuid=True), ForeignKey("proveedores.id_proveedor"), nullable=False
    )

    # Auditoría
    creado_en = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    actualizado_en = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    creado_por = Column(String(100), nullable=True)
    actualizado_por = Column(String(100), nullable=True)

    categoria = relationship("Categoria", back_populates="productos")
    proveedor = relationship("Proveedor", back_populates="productos")
    detalles = relationship("DetalleCompra", back_populates="producto")

    def __repr__(self):
        return f"<​Producto(nombre='{self.nombre}', precio={self.precio}, activo={self.activo})>"
