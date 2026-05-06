# src/enpoints/app.py

import sys
import os

# Agregar el directorio padre al path para resolver imports relativos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from enpoints.categoria import router as categoria_router
from enpoints.producto import router as producto_router
from enpoints.cliente import router as cliente_router
from enpoints.proveedor import router as proveedor_router
from enpoints.empleado import router as empleado_router
from enpoints.caja_registradora import router as caja_registradora_router
from enpoints.compra import router as compra_router
from enpoints.detalle_compra import router as detalle_compra_router
from enpoints.jornada import router as jornada_router
from enpoints.pago import router as pago_router

from database.config import create_tables

# Crear instancia principal de FastAPI
app = FastAPI(title="API Supermercado", version="1.0.0")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",
        "http://127.0.0.1:4200",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === REGISTRAR TODOS LOS ROUTERS AQUÍ ===
app.include_router(categoria_router, prefix="/categorias", tags=["categorias"])
app.include_router(producto_router, prefix="/productos", tags=["productos"])
app.include_router(cliente_router, prefix="/clientes", tags=["clientes"])
app.include_router(proveedor_router, prefix="/proveedores", tags=["proveedores"])
app.include_router(empleado_router, prefix="/empleados", tags=["empleados"])
app.include_router(caja_registradora_router, prefix="/cajas", tags=["cajas"])
app.include_router(compra_router, prefix="/compras", tags=["compras"])
app.include_router(
    detalle_compra_router, prefix="/detalles_compra", tags=["detalles_compra"]
)
app.include_router(jornada_router, prefix="/jornadas", tags=["jornadas"])
app.include_router(pago_router, prefix="/pagos", tags=["pagos"])
# === FIN DEL REGISTRO DE ROUTERS ===


# === ENDPOINTS GENERALES ===
@app.get("/")
def root():
    return {"mensaje": "Bienvenido al Backend del Supermercado"}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
