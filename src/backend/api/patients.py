from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Security, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.database import get_db
from src.database.models import Patient
from src.database.repository import BaseRepository
from src.backend.schemas import PatientCreate, PatientResponse
from src.backend.security.dependencies import get_current_user, TokenData

router = APIRouter(prefix="/api/v1/patients", tags=["patients"])

def get_patient_repo(db: AsyncSession = Depends(get_db)) -> BaseRepository[Patient]:
    return BaseRepository(Patient, db)

@router.post("/", response_model=PatientResponse, status_code=status.HTTP_201_CREATED)
async def create_patient(
    patient_in: PatientCreate,
    current_user: Annotated[TokenData, Security(get_current_user, scopes=["admin:all"])],
    repo: BaseRepository[Patient] = Depends(get_patient_repo)
):
    new_patient = await repo.create(patient_in.model_dump())
    return new_patient

@router.get("/{patient_id}", response_model=PatientResponse)
async def get_patient(
    patient_id: str,
    current_user: Annotated[TokenData, Security(get_current_user, scopes=["patients:read"])],
    repo: BaseRepository[Patient] = Depends(get_patient_repo)
):
    patient = await repo.get(patient_id)
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Paciente no encontrado o eliminado"
        )
    return patient

@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_patient(
    patient_id: str,
    current_user: Annotated[TokenData, Security(get_current_user, scopes=["admin:all"])],
    repo: BaseRepository[Patient] = Depends(get_patient_repo)
):
    success = await repo.soft_delete(patient_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Error: Paciente no existe en base activa."
        )
