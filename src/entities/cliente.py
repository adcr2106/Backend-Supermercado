import sys
import os
import uuid

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database.config import Base
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func


class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    documento = Column(String(50), nullable=False, unique=True)
    nombre = Column(String(100), nullable=False)
    telefono = Column(String(20), nullable=True)
    correo = Column(String(100), nullable=True, unique=True)
    activo = Column(Boolean, nullable=False, default=True)

    # Auditoría
    creado_en = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    actualizado_en = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    creado_por = Column(String(100), nullable=True)
    actualizado_por = Column(String(100), nullable=True)

    def __repr__(self):
        return f"<​Cliente(nombre='{self.nombre}', documento='{self.documento}', activo={self.activo})>"
