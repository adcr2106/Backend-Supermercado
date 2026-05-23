import sys
import os
import uuid

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database.config import Base
from sqlalchemy import Column, Boolean
from sqlalchemy.dialects.postgresql import UUID


class CajaRegistradora(Base):
    __tablename__ = "cajas_registradoras"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    activo = Column(Boolean, nullable=False, default=True)

    def __repr__(self):
        return f"<​CajaRegistradora(id={self.id}, activo={self.activo})>"
