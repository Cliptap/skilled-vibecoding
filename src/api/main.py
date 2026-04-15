from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routers import pacientes, citas, reportes
from src.api.db.database import engine, Base
from src.api.db import models

# Asegurarnos de que las tablas en SQLite existan
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Solucionar error de conectividad (CORS) con React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pacientes.router)
app.include_router(citas.router)
app.include_router(reportes.router)
