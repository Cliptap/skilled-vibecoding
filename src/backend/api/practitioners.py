from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Security, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from src.database.database import get_db
from src.database.models import Practitioner
from src.database.repository import BaseRepository
from src.backend.schemas import PractitionerCreate, PractitionerResponse
from src.backend.security.dependencies import get_current_user, TokenData

router = APIRouter(prefix="/api/v1/practitioners", tags=["practitioners"])

class PractitionerRepository(BaseRepository[Practitioner]):
    def __init__(self, session: AsyncSession):
        super().__init__(Practitioner, session)

@router.post("/", response_model=PractitionerResponse, status_code=status.HTTP_201_CREATED)
async def create_practitioner(
    practitioner_in: PractitionerCreate, 
    current_user: Annotated[TokenData, Security(get_current_user, scopes=["admin:all"])],
    db: AsyncSession = Depends(get_db)):
    repo = PractitionerRepository(db)
    return await repo.create(practitioner_in.model_dump())

@router.get("/", response_model=list[PractitionerResponse])
async def get_all_practitioners(
    current_user: Annotated[TokenData, Security(get_current_user, scopes=["patients:read"])],
    db: AsyncSession = Depends(get_db)):
    repo = PractitionerRepository(db)
    practitioners = await repo.get_all()
    return list(practitioners)

@router.get("/{practitioner_id}", response_model=PractitionerResponse)
async def get_practitioner(
    practitioner_id: str, 
    current_user: Annotated[TokenData, Security(get_current_user, scopes=["patients:read"])],
    db: AsyncSession = Depends(get_db)):
    repo = PractitionerRepository(db)
    practitioner = await repo.get(practitioner_id)
    if not practitioner:
        raise HTTPException(status_code=404, detail="Practitioner not found")
    return practitioner

@router.delete("/{practitioner_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_practitioner(
    practitioner_id: str,
    current_user: Annotated[TokenData, Security(get_current_user, scopes=["admin:all"])],
    db: AsyncSession = Depends(get_db)):
    repo = PractitionerRepository(db)
    success = await repo.soft_delete(practitioner_id)
    if not success:
        raise HTTPException(status_code=404, detail="Practitioner no encontrado")
