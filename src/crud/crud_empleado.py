"""
Operaciones CRUD para Empleado
"""

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from typing import List, Optional
from uuid import UUID

from entities.empleado import Empleado
from sqlalchemy.orm import Session


class EmpleadoCRUD:
    def __init__(self, db: Session):
        self.db = db

    def crear_empleado(
        self,
        documento: str,
        nombre: str,
        salario: float,
        cargo: str,
        contrasena: str,
        telefono: str = None,
        correo: str = None,
        creado_por: str = None,
    ) -> Empleado:
        if not documento or len(documento.strip()) == 0:
            raise ValueError("El documento del empleado es obligatorio")
        if len(documento) > 50:
            raise ValueError("El documento no puede exceder 50 caracteres")

        if not nombre or len(nombre.strip()) == 0:
            raise ValueError("El nombre del empleado es obligatorio")
        if len(nombre) > 100:
            raise ValueError("El nombre no puede exceder 100 caracteres")

        if salario is None or salario < 0:
            raise ValueError("El salario debe ser un valor positivo")

        if not cargo or len(cargo.strip()) == 0:
            raise ValueError("El cargo del empleado es obligatorio")
        if len(cargo) > 50:
            raise ValueError("El cargo no puede exceder 50 caracteres")

        if not contrasena or len(contrasena.strip()) == 0:
            raise ValueError("La contraseña es obligatoria")
        if len(contrasena) > 20:
            raise ValueError("La contraseña no puede exceder 20 caracteres")

        if self.obtener_empleado_por_documento(documento, incluir_inactivos=True):
            raise ValueError("Ya existe un empleado con ese documento")

        if correo and self.obtener_empleado_por_correo(correo, incluir_inactivos=True):
            raise ValueError("Ya existe un empleado con ese correo")

        empleado = Empleado(
            documento=documento.strip(),
            nombre=nombre.strip(),
            salario=salario,
            cargo=cargo.strip(),
            contrasena=contrasena.strip(),
            telefono=telefono.strip() if telefono else None,
            correo=correo.strip() if correo else None,
            creado_por=creado_por.strip() if creado_por else None,
            activo=True,
        )
        self.db.add(empleado)
        self.db.commit()
        self.db.refresh(empleado)
        return empleado

    def obtener_empleado(
        self, empleado_id: UUID, incluir_inactivos: bool = False
    ) -> Optional[Empleado]:
        query = self.db.query(Empleado).filter(Empleado.id == empleado_id)
        if not incluir_inactivos:
            query = query.filter(Empleado.activo.is_(True))
        return query.first()

    def obtener_empleado_por_documento(
        self, documento: str, incluir_inactivos: bool = False
    ) -> Optional[Empleado]:
        query = self.db.query(Empleado).filter(Empleado.documento == documento.strip())
        if not incluir_inactivos:
            query = query.filter(Empleado.activo.is_(True))
        return query.first()

    def obtener_empleado_por_correo(
        self, correo: str, incluir_inactivos: bool = False
    ) -> Optional[Empleado]:
        query = self.db.query(Empleado).filter(Empleado.correo == correo.strip())
        if not incluir_inactivos:
            query = query.filter(Empleado.activo.is_(True))
        return query.first()

    def autenticar_empleado(
        self, documento: str, contrasena: str
    ) -> Optional[Empleado]:
        return (
            self.db.query(Empleado)
            .filter(
                Empleado.documento == documento.strip(),
                Empleado.contrasena == contrasena.strip(),
                Empleado.activo.is_(True),
            )
            .first()
        )

    def obtener_empleados(
        self, skip: int = 0, limit: int = 100, incluir_inactivos: bool = False
    ) -> List[Empleado]:
        query = self.db.query(Empleado)
        if not incluir_inactivos:
            query = query.filter(Empleado.activo.is_(True))
        return query.offset(skip).limit(limit).all()

    def actualizar_empleado(
        self, empleado_id: UUID, actualizado_por: str = None, **kwargs
    ) -> Optional[Empleado]:
        empleado = self.obtener_empleado(empleado_id, incluir_inactivos=True)
        if not empleado:
            return None

        if "documento" in kwargs:
            documento = kwargs["documento"]
            if not documento or len(documento.strip()) == 0:
                raise ValueError("El documento es obligatorio")
            if len(documento) > 50:
                raise ValueError("El documento no puede exceder 50 caracteres")
            existente = self.obtener_empleado_por_documento(
                documento, incluir_inactivos=True
            )
            if existente and existente.id != empleado_id:
                raise ValueError("Ya existe un empleado con ese documento")
            kwargs["documento"] = documento.strip()

        if "nombre" in kwargs:
            nombre = kwargs["nombre"]
            if not nombre or len(nombre.strip()) == 0:
                raise ValueError("El nombre es obligatorio")
            if len(nombre) > 100:
                raise ValueError("El nombre no puede exceder 100 caracteres")
            kwargs["nombre"] = nombre.strip()

        if "salario" in kwargs:
            if kwargs["salario"] is None or kwargs["salario"] < 0:
                raise ValueError("El salario debe ser un valor positivo")

        if "cargo" in kwargs:
            cargo = kwargs["cargo"]
            if not cargo or len(cargo.strip()) == 0:
                raise ValueError("El cargo es obligatorio")
            if len(cargo) > 50:
                raise ValueError("El cargo no puede exceder 50 caracteres")
            kwargs["cargo"] = cargo.strip()

        if "contrasena" in kwargs:
            contrasena = kwargs["contrasena"]
            if not contrasena or len(contrasena.strip()) == 0:
                raise ValueError("La contraseña es obligatoria")
            if len(contrasena) > 20:
                raise ValueError("La contraseña no puede exceder 20 caracteres")
            kwargs["contrasena"] = contrasena.strip()

        if "correo" in kwargs and kwargs["correo"]:
            correo = kwargs["correo"]
            existente = self.obtener_empleado_por_correo(correo, incluir_inactivos=True)
            if existente and existente.id != empleado_id:
                raise ValueError("Ya existe un empleado con ese correo")
            kwargs["correo"] = correo.strip()

        if "telefono" in kwargs and kwargs["telefono"]:
            kwargs["telefono"] = kwargs["telefono"].strip()

        for key, value in kwargs.items():
            if hasattr(empleado, key):
                setattr(empleado, key, value)

        if actualizado_por:
            empleado.actualizado_por = actualizado_por.strip()

        self.db.commit()
        self.db.refresh(empleado)
        return empleado

    def eliminar_empleado(self, empleado_id: UUID) -> bool:
        empleado = self.obtener_empleado(empleado_id, incluir_inactivos=True)
        if empleado and empleado.activo:
            empleado.activo = False
            self.db.commit()
            return True
        return False

    def activar_empleado(self, empleado_id: UUID) -> bool:
        empleado = self.obtener_empleado(empleado_id, incluir_inactivos=True)
        if empleado and not empleado.activo:
            empleado.activo = True
            self.db.commit()
            return True
        return False
