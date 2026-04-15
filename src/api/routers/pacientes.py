from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from src.api.schemas.paciente import PacienteCreate, PacienteUpdate, PacienteOut
from src.api.db import models, database
from typing import List

router = APIRouter(prefix="/pacientes", tags=["Pacientes"])

# Dependency
get_db = database.SessionLocal

def get_session():
    db = get_db()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=PacienteOut, status_code=201)
def create_paciente(paciente: PacienteCreate, db: Session = Depends(get_session)):
    db_paciente = models.Paciente(**paciente.dict())
    db.add(db_paciente)
    db.commit()
    db.refresh(db_paciente)
    return db_paciente

@router.get("/", response_model=List[PacienteOut])
def list_pacientes(db: Session = Depends(get_session)):
    return db.query(models.Paciente).all()

@router.get("/{paciente_id}", response_model=PacienteOut)
def get_paciente(paciente_id: int, db: Session = Depends(get_session)):
    paciente = db.query(models.Paciente).filter(models.Paciente.id == paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return paciente

@router.put("/{paciente_id}", response_model=PacienteOut)
def update_paciente(paciente_id: int, paciente: PacienteUpdate, db: Session = Depends(get_session)):
    db_paciente = db.query(models.Paciente).filter(models.Paciente.id == paciente_id).first()
    if not db_paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    for key, value in paciente.dict(exclude_unset=True).items():
        setattr(db_paciente, key, value)
    db.commit()
    db.refresh(db_paciente)
    return db_paciente

@router.delete("/{paciente_id}", status_code=204)
def delete_paciente(paciente_id: int, db: Session = Depends(get_session)):
    paciente = db.query(models.Paciente).filter(models.Paciente.id == paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    db.delete(paciente)
    db.commit()
    return

@router.get("/buscar/{rut}", response_model=PacienteOut)
def buscar_paciente_por_rut(rut: str, db: Session = Depends(get_session)):
    paciente = db.query(models.Paciente).filter(models.Paciente.rut == rut).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return paciente
