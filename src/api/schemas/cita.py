from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CitaBase(BaseModel):
    paciente_id: int
    fecha: datetime
    razon: Optional[str] = None

class CitaCreate(CitaBase):
    pass

class CitaUpdate(CitaBase):
    pass

class CitaOut(CitaBase):
    id: int

    class Config:
        orm_mode = True
