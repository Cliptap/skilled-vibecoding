from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import date

class PacienteBase(BaseModel):
    nombre: str
    apellido: str
    rut: str
    telefono: Optional[str] = None
    correo: Optional[EmailStr] = None
    sexo: Optional[str] = None
    fecha_nacimiento: Optional[date] = None
    prevision: Optional[str] = None

    @validator('nombre', 'apellido')
    def format_names(cls, v):
        if v:
            return ' '.join(v.split()).title()
        return v

    @validator('rut')
    def validate_and_format_rut(cls, v):
        rut_clean = str(v).replace(".", "").replace("-", "").strip().upper()
        if not rut_clean or len(rut_clean) < 2:
            raise ValueError("El RUT no tiene un formato válido")
        
        cuerpo = rut_clean[:-1]
        dv = rut_clean[-1]
        
        if not cuerpo.isdigit():
            raise ValueError("El cuerpo del RUT debe ser numérico")
        
        suma = 0
        multiplo = 2
        for c in reversed(cuerpo):
            suma += int(c) * multiplo
            multiplo += 1
            if multiplo == 8:
                multiplo = 2
        
        dv_esperado = 11 - (suma % 11)
        dv_calc = '0' if dv_esperado == 11 else ('K' if dv_esperado == 10 else str(dv_esperado))
        
        if dv != dv_calc:
            raise ValueError("El RUT ingresado no es válido (Dígito verificador incorrecto)")
            
        return f"{cuerpo}-{dv}"

class PacienteCreate(PacienteBase):
    pass

class PacienteUpdate(PacienteBase):
    pass

class PacienteOut(PacienteBase):
    id: int

    class Config:
        orm_mode = True
