"""
Arranca la API FastAPI (uvicorn).rando e

  python main.py

Documentación interactiva: http://127.0.0.1:8000/docs

Para crear tablas en la base de datos, usa: python init_db.py
"""

import uvicorn

from src.enpoints.app import app

if __name__ == "__main__":
    # reload exige el string de importación; `app` sigue disponible para tests / ASGI
    uvicorn.run(
        "src.enpoints.app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
