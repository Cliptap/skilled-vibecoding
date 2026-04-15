from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import Base

class Paciente(Base):
    __tablename__ = "paciente"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    nombre = Column(Text, nullable=False)
    apellido = Column(Text, nullable=False)
    rut = Column(Text, unique=True, nullable=False, index=True)
    telefono = Column(Text)
    correo = Column(Text)
    sexo = Column(Text)
    fecha_nacimiento = Column(Date)
    prevision = Column(Text)
    citas = relationship("Cita", back_populates="paciente", cascade="all, delete-orphan")

class Cita(Base):
    __tablename__ = "cita"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    paciente_id = Column(Integer, ForeignKey("paciente.id", ondelete="CASCADE"), nullable=False, index=True)
    fecha = Column(DateTime(timezone=True), nullable=False, index=True)
    razon = Column(Text)
    paciente = relationship("Paciente", back_populates="citas")
