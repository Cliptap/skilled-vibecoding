from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from src.backend.security.auth import create_access_token, verify_password, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(tags=["auth"])

# Mock de base de datos de usuarios para el MVP de Alta Gobernanza
# En un sistema real esto vendría de la base de datos
FAKE_USERS_DB = {
    "admin@clinic.com": {
        "username": "admin@clinic.com",
        "hashed_password": "$2b$12$EdsBxPpHdZjTyHLl4h1RvO6PF5w.4TZoUoWQxS1vjJGJ7iwnAzK0y", # 'admin123'
        "scopes": ["admin:all", "patients:read", "appointments:write", "appointments:read"],
    }
}

@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = FAKE_USERS_DB.get(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"], "scopes": user["scopes"]},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
