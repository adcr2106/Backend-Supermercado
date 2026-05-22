import sys
import os
import uuid

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database.config import Base
from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class Proveedor(Base):
    __tablename__ = "proveedores"

    id_proveedor = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    nombre = Column(String(100), nullable=False)
    activo = Column(Boolean, nullable=False, default=True)

    productos = relationship("Producto", back_populates="proveedor")

    def __repr__(self):
        return f"<​Proveedor(nombre='{self.nombre}', activo={self.activo})>"
