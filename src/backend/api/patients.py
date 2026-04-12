from typing import List
from fastapi import APIRouter, HTTPException, status
from ..schemas.patient import PatientCreate, PatientUpdate, PatientResponse
from ..services.patient_service import PatientService

router = APIRouter(prefix="/patients", tags=["patients"])
service = PatientService()

@router.get("/stats/kpis", status_code=status.HTTP_200_OK)
def get_patient_stats(time_filter: str = 'all'):
    return service.get_stats(time_filter)

@router.get("/", response_model=List[PatientResponse], status_code=status.HTTP_200_OK)
def list_patients(time_filter: str = 'all', sort: str = 'desc'):
    return service.list_patients(time_filter, sort)

@router.post("/", response_model=PatientResponse, status_code=status.HTTP_201_CREATED)
def create_patient(patient: PatientCreate):
    existing = service.get_patient_by_rut(patient.rut)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Ya existe un paciente registrado con este RUT"
        )
    return service.create_patient(patient)

@router.get("/{rut}", response_model=PatientResponse, status_code=status.HTTP_200_OK)
def get_patient(rut: str):
    patient = service.get_patient_by_rut(rut)
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Paciente no encontrado"
        )
    return patient

@router.put("/{rut}", response_model=PatientResponse, status_code=status.HTTP_200_OK)
def update_patient(rut: str, patient_update: PatientUpdate):
    patient = service.update_patient(rut, patient_update)
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Paciente no encontrado para actualizar"
        )
    return patient

@router.delete("/{rut}", status_code=status.HTTP_204_NO_CONTENT)
def delete_patient(rut: str):
    success = service.delete_patient(rut)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Paciente no encontrado para eliminar"
        )
    return
