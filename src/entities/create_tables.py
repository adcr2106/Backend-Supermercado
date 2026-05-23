#!/usr/bin/env python3
"""
Script para crear tablas y verificar conexión con Neon
"""

import os
import sys

# 🔧 Ajustar path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dotenv import load_dotenv
from sqlalchemy import text
from database.config import Base, engine

# 🔥 IMPORTAR TODOS LOS MODELOS
from caja_registradora import CajaRegistradora
from categoria import Categoria
from cliente import Cliente
from compra import Compra
from detalle_compra import DetalleCompra
from empleado import Empleado
from jornada import Jornada
from pago import Pago
from producto import Producto
from proveedor import Proveedor


def diagnostico():
    """Diagnóstico completo de conexión"""
    print("\n🔍 === DIAGNÓSTICO ===")

    try:
        with engine.connect() as conn:
            # 📌 Base de datos actual
            db = conn.execute(text("SELECT current_database();")).scalar()
            print("📌 Base de datos:", db)

            # 👤 Usuario
            user = conn.execute(text("SELECT current_user;")).scalar()
            print("👤 Usuario:", user)

            # 📦 Tablas existentes
            print("\n📦 Tablas en la BD:")
            result = conn.execute(
                text(
                    """
                SELECT table_schema, table_name
                FROM information_schema.tables
                WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
                ORDER BY table_schema, table_name;
            """
                )
            )

            tables = result.fetchall()
            if tables:
                for row in tables:
                    print(f"  {row[0]}.{row[1]}")
            else:
                print("  ⚠️ No hay tablas en la base de datos")

    except Exception as e:
        print("❌ Error en diagnóstico:", e)


def verificar_modelos():
    """Verifica que SQLAlchemy detecta los modelos"""
    print("\n📦 === MODELOS REGISTRADOS ===")

    if Base.metadata.tables:
        for table in Base.metadata.tables.keys():
            print(f"  ✔ {table}")
    else:
        print("❌ No hay modelos registrados (problema de imports)")


def crear_tablas():
    """Crear todas las tablas"""
    try:
        print("\n🚀 Creando tablas...")

        Base.metadata.create_all(bind=engine)

        print("✅ Tablas creadas (o ya existían)")
        return True

    except Exception as e:
        print(f"❌ Error al crear tablas: {e}")
        return False


def prueba_escritura():
    """Prueba directa creando una tabla manual"""
    print("\n🧪 === PRUEBA DIRECTA ===")

    try:
        with engine.connect() as conn:
            conn.execute(text("CREATE TABLE IF NOT EXISTS prueba_chatgpt (id INT);"))
            conn.commit()
            print("✅ Tabla 'prueba_chatgpt' creada correctamente")

    except Exception as e:
        print("❌ Error en prueba directa:", e)


def main():
    """Función principal"""
    print("🔥 INICIANDO SCRIPT DE TABLAS 🔥")

    # 📥 Cargar variables de entorno
    load_dotenv()

    # 🔍 Ver DATABASE_URL
    db_url = os.getenv("DATABASE_URL")
    print("\n🌐 DATABASE_URL:", db_url)

    if not db_url:
        print("❌ ERROR: DATABASE_URL no está configurada")
        return

    # 🔍 Ver engine real
    print("🔗 Engine URL:", engine.url)

    # 🔍 Verificar modelos
    verificar_modelos()

    # 🔍 Diagnóstico antes
    diagnostico()

    # 🚀 Crear tablas
    if crear_tablas():
        # 🧪 Prueba directa
        prueba_escritura()

        # 🔍 Diagnóstico después
        diagnostico()
    else:
        print("❌ No se pudieron crear las tablas")


if __name__ == "__main__":
    main()
