from contextlib import asynccontextmanager
from fastapi import FastAPI
from asgi_correlation_id import CorrelationIdMiddleware

from src.database.database import engine, Base
from src.backend.api.patients import router as patients_router
from src.backend.api.secure_example import router as secure_router
from src.backend.api.practitioners import router as practitioners_router
from src.backend.api.appointments import router as appointments_router

import src.database.events # Registra Soft Deletes y Auditoria

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()

app = FastAPI(
    title="VibeCoding Clinic API - Alta Gobernanza",
    version="3.0.0",
    lifespan=lifespan
)

app.add_middleware(CorrelationIdMiddleware)

app.include_router(patients_router)
app.include_router(practitioners_router)
app.include_router(appointments_router)
app.include_router(secure_router)

@app.get("/health", tags=["system"])
def health_check():
    return {"status": "healthy"}
