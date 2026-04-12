from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from src.backend.api.patients import router as patients_router

app = FastAPI(
    title="Consultorio API",
    description="API de gestión para fichas de pacientes. Gobernanza nivel Baja.",
    version="1.0.0"
)

# Configurar CORS para permitir que el Frontend consuma la API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir local
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Lista de IPs permitidas (Gobernanza de acceso requerida por PRD)
# Por defecto se deja el localhost para entorno de pruebas/recepcionista
ALLOWED_IPS = {"127.0.0.1", "::1", "testclient"}

@app.middleware("http")
async def ip_restriction_middleware(request: Request, call_next):
    # Validar si el cliente está en la lista de IPs permitidas (manejando possible None en pruebas unitarias)
    client_ip = request.client.host if request.client else "127.0.0.1"
    
    if client_ip not in ALLOWED_IPS:
        return JSONResponse(
            status_code=403,
            content={"detail": "Acceso denegado: IP no autorizada."}
        )
    response = await call_next(request)
    return response

# Incluir Rutas
app.include_router(patients_router)

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Consultorio API Funcionando"}
