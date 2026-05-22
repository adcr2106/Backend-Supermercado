"""
Operaciones CRUD para Cliente
"""

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from typing import List, Optional
from uuid import UUID

from entities.cliente import Cliente
from sqlalchemy.orm import Session


class ClienteCRUD:
    def __init__(self, db: Session):
        self.db = db

    def crear_cliente(
        self,
        documento: str,
        nombre: str,
        telefono: str = None,
        correo: str = None,
        creado_por: str = None,
    ) -> Cliente:
        if not documento or len(documento.strip()) == 0:
            raise ValueError("El documento del cliente es obligatorio")
        if len(documento) > 50:
            raise ValueError("El documento no puede exceder 50 caracteres")

        if not nombre or len(nombre.strip()) == 0:
            raise ValueError("El nombre del cliente es obligatorio")
        if len(nombre) > 100:
            raise ValueError("El nombre no puede exceder 100 caracteres")

        if self.obtener_cliente_por_documento(documento, incluir_inactivos=True):
            raise ValueError("Ya existe un cliente con ese documento")

        if correo and self.obtener_cliente_por_correo(correo, incluir_inactivos=True):
            raise ValueError("Ya existe un cliente con ese correo")

        cliente = Cliente(
            documento=documento.strip(),
            nombre=nombre.strip(),
            telefono=telefono.strip() if telefono else None,
            correo=correo.strip() if correo else None,
            creado_por=creado_por.strip() if creado_por else None,
            activo=True,
        )
        self.db.add(cliente)
        self.db.commit()
        self.db.refresh(cliente)
        return cliente

    def obtener_cliente(
        self, cliente_id: UUID, incluir_inactivos: bool = False
    ) -> Optional[Cliente]:
        query = self.db.query(Cliente).filter(Cliente.id == cliente_id)
        if not incluir_inactivos:
            query = query.filter(Cliente.activo.is_(True))
        return query.first()

    def obtener_cliente_por_documento(
        self, documento: str, incluir_inactivos: bool = False
    ) -> Optional[Cliente]:
        query = self.db.query(Cliente).filter(Cliente.documento == documento.strip())
        if not incluir_inactivos:
            query = query.filter(Cliente.activo.is_(True))
        return query.first()

    def obtener_cliente_por_correo(
        self, correo: str, incluir_inactivos: bool = False
    ) -> Optional[Cliente]:
        query = self.db.query(Cliente).filter(Cliente.correo == correo.strip())
        if not incluir_inactivos:
            query = query.filter(Cliente.activo.is_(True))
        return query.first()

    def obtener_clientes(
        self, skip: int = 0, limit: int = 100, incluir_inactivos: bool = False
    ) -> List[Cliente]:
        query = self.db.query(Cliente)
        if not incluir_inactivos:
            query = query.filter(Cliente.activo.is_(True))
        return query.offset(skip).limit(limit).all()

    def actualizar_cliente(
        self, cliente_id: UUID, actualizado_por: str = None, **kwargs
    ) -> Optional[Cliente]:
        cliente = self.obtener_cliente(cliente_id, incluir_inactivos=True)
        if not cliente:
            return None

        if "documento" in kwargs:
            documento = kwargs["documento"]
            if not documento or len(documento.strip()) == 0:
                raise ValueError("El documento es obligatorio")
            if len(documento) > 50:
                raise ValueError("El documento no puede exceder 50 caracteres")
            existente = self.obtener_cliente_por_documento(
                documento, incluir_inactivos=True
            )
            if existente and existente.id != cliente_id:
                raise ValueError("Ya existe un cliente con ese documento")
            kwargs["documento"] = documento.strip()

        if "nombre" in kwargs:
            nombre = kwargs["nombre"]
            if not nombre or len(nombre.strip()) == 0:
                raise ValueError("El nombre es obligatorio")
            if len(nombre) > 100:
                raise ValueError("El nombre no puede exceder 100 caracteres")
            kwargs["nombre"] = nombre.strip()

        if "correo" in kwargs and kwargs["correo"]:
            correo = kwargs["correo"]
            existente = self.obtener_cliente_por_correo(correo, incluir_inactivos=True)
            if existente and existente.id != cliente_id:
                raise ValueError("Ya existe un cliente con ese correo")
            kwargs["correo"] = correo.strip()

        if "telefono" in kwargs and kwargs["telefono"]:
            kwargs["telefono"] = kwargs["telefono"].strip()

        for key, value in kwargs.items():
            if hasattr(cliente, key):
                setattr(cliente, key, value)

        if actualizado_por:
            cliente.actualizado_por = actualizado_por.strip()

        self.db.commit()
        self.db.refresh(cliente)
        return cliente

    def eliminar_cliente(self, cliente_id: UUID) -> bool:
        cliente = self.obtener_cliente(cliente_id, incluir_inactivos=True)
        if cliente and cliente.activo:
            cliente.activo = False
            self.db.commit()
            return True
        return False

    def activar_cliente(self, cliente_id: UUID) -> bool:
        cliente = self.obtener_cliente(cliente_id, incluir_inactivos=True)
        if cliente and not cliente.activo:
            cliente.activo = True
            self.db.commit()
            return True
        return False
