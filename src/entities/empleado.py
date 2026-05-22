import sys
import os
import uuid

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database.config import Base
from sqlalchemy import Column, String, Numeric, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, validates
from sqlalchemy.sql import func


class Empleado(Base):
    __tablename__ = "empleados"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    documento = Column(String(50), nullable=False, unique=True)
    nombre = Column(String(100), nullable=False)
    salario = Column(Numeric(10, 2), nullable=False)
    cargo = Column(String(50), nullable=False)
    telefono = Column(String(20), nullable=True)
    correo = Column(String(100), nullable=True, unique=True)
    contrasena = Column(String(20), nullable=False)
    activo = Column(Boolean, nullable=False, default=True)

    # Auditoría
    creado_en = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    actualizado_en = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    creado_por = Column(String(100), nullable=True)
    actualizado_por = Column(String(100), nullable=True)

    compras = relationship("Compra", back_populates="empleado")

    @validates("cargo")
    def convert_mayus(self, key, value):
        return value.upper()

    def __repr__(self):
        return f"<​Empleado(nombre='{self.nombre}', cargo='{self.cargo}', activo={self.activo})>"
