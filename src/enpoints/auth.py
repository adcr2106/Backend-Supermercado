"""
API de Autenticación - Endpoints para login y autenticación de empleados
"""

from uuid import UUID

from crud.crud_empleado import EmpleadoCRUD
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from schemas import EmpleadoResponse, LoginEmpleado, RespuestaAPI
from sqlalchemy.orm import Session

router = APIRouter(prefix="/auth", tags=["autenticación"])


@router.post("/login", response_model=EmpleadoResponse)
async def login(login_data: LoginEmpleado, db: Session = Depends(get_db)):
    """Autenticar un empleado con documento y contraseña."""
    try:
        empleado_crud = EmpleadoCRUD(db)
        empleado = empleado_crud.autenticar_empleado(
            login_data.documento, login_data.contrasena
        )

        if not empleado:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales incorrectas o empleado inactivo",
            )

        return empleado
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error durante el login: {str(e)}",
        )


@router.get("/verificar/{empleado_id}", response_model=RespuestaAPI)
async def verificar_empleado(empleado_id: UUID, db: Session = Depends(get_db)):
    """Verificar si un empleado existe y está activo."""
    try:
        empleado_crud = EmpleadoCRUD(db)
        empleado = empleado_crud.obtener_empleado(empleado_id)

        if not empleado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Empleado no encontrado",
            )

        return RespuestaAPI(
            mensaje="Empleado verificado exitosamente",
            exito=True,
            datos={
                "empleado_id": str(empleado.id),
                "documento": empleado.documento,
                "nombre": empleado.nombre,
                "correo": empleado.correo,
                "cargo": empleado.cargo,
                "activo": empleado.activo,
            },
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al verificar empleado: {str(e)}",
        )


@router.get("/estado", response_model=RespuestaAPI)
async def estado_autenticacion():
    """Verificar el estado del sistema de autenticación."""
    return RespuestaAPI(
        mensaje="Sistema de autenticación funcionando correctamente",
        exito=True,
        datos={
            "sistema": "Sistema de Gestión de Supermercado",
            "version": "1.0.0",
            "autenticacion": "Activa",
        },
    )
