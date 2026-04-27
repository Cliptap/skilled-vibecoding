from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Security, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from src.database.database import get_db
from src.database.models import Appointment
from src.database.repository import BaseRepository
from src.backend.schemas import AppointmentCreate, AppointmentResponse
from src.backend.security.dependencies import get_current_user, TokenData

router = APIRouter(prefix="/api/v1/appointments", tags=["appointments"])

class AppointmentRepository(BaseRepository[Appointment]):
    def __init__(self, session: AsyncSession):
        super().__init__(Appointment, session)

@router.post("/", response_model=AppointmentResponse, status_code=status.HTTP_201_CREATED)
async def create_appointment(
    appointment_in: AppointmentCreate, 
    current_user: Annotated[TokenData, Security(get_current_user, scopes=["admin:all"])],
    db: AsyncSession = Depends(get_db)):
    repo = AppointmentRepository(db)
    return await repo.create(appointment_in.model_dump())

@router.get("/{appointment_id}", response_model=AppointmentResponse)
async def get_appointment(
    appointment_id: str, 
    current_user: Annotated[TokenData, Security(get_current_user, scopes=["patients:read"])],
    db: AsyncSession = Depends(get_db)):
    repo = AppointmentRepository(db)
    appointment = await repo.get(appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment
