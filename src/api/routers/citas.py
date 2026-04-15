from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from src.api.schemas.cita import CitaCreate, CitaUpdate, CitaOut
from src.api.db import models, database
from typing import List

router = APIRouter(prefix="/citas", tags=["Citas"])

# Dependency
get_db = database.SessionLocal

def get_session():
    db = get_db()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=CitaOut, status_code=201)
def create_cita(cita: CitaCreate, db: Session = Depends(get_session)):
    db_cita = models.Cita(**cita.dict())
    db.add(db_cita)
    db.commit()
    db.refresh(db_cita)
    return db_cita

@router.get("/", response_model=List[CitaOut])
def list_citas(db: Session = Depends(get_session)):
    return db.query(models.Cita).all()

@router.get("/{cita_id}", response_model=CitaOut)
def get_cita(cita_id: int, db: Session = Depends(get_session)):
    cita = db.query(models.Cita).filter(models.Cita.id == cita_id).first()
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    return cita

@router.put("/{cita_id}", response_model=CitaOut)
def update_cita(cita_id: int, cita: CitaUpdate, db: Session = Depends(get_session)):
    db_cita = db.query(models.Cita).filter(models.Cita.id == cita_id).first()
    if not db_cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    for key, value in cita.dict(exclude_unset=True).items():
        setattr(db_cita, key, value)
    db.commit()
    db.refresh(db_cita)
    return db_cita

@router.delete("/{cita_id}", status_code=204)
def delete_cita(cita_id: int, db: Session = Depends(get_session)):
    cita = db.query(models.Cita).filter(models.Cita.id == cita_id).first()
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    db.delete(cita)
    db.commit()
    return

@router.get("/por_fecha/{fecha}", response_model=List[CitaOut])
def listar_citas_por_fecha(fecha: str, db: Session = Depends(get_session)):
    citas = db.query(models.Cita).filter(models.Cita.fecha.cast("date") == fecha).all()
    return citas
