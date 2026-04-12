from datetime import datetime
from typing import Optional
from ..schemas.patient import PatientCreate, PatientUpdate

# TODO: Reemplazar este diccionario en memoria por conexión a PostgreSQL (Ej: psycopg2, asyncpg, o SQLAlchemy)
# Se utiliza un store en memoria para cumplir la separación de capas y permitir pruebas del endpoint de forma aislada.
_mock_db = {}
_id_counter = 1

class PatientService:
    def get_patient_by_rut(self, rut: str) -> Optional[dict]:
        return _mock_db.get(rut)

    def create_patient(self, data: PatientCreate) -> dict:
        global _id_counter
        now = datetime.utcnow().isoformat()
        patient_record = data.dict()
        patient_record.update({
            "patient_id": _id_counter,
            "created_at": now,
            "updated_at": now
        })
        _mock_db[data.rut] = patient_record
        _id_counter += 1
        return patient_record

    def update_patient(self, rut: str, data: PatientUpdate) -> Optional[dict]:
        patient = self.get_patient_by_rut(rut)
        if not patient:
            return None
        
        update_data = data.dict(exclude_unset=True)
        if update_data:
            patient.update(update_data)
            patient["updated_at"] = datetime.utcnow().isoformat()
            _mock_db[rut] = patient
            
        return patient

    def delete_patient(self, rut: str) -> bool:
        if rut in _mock_db:
            del _mock_db[rut]
            return True
        return False
