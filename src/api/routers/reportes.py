from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from src.api.db import database

router = APIRouter(prefix="/reportes", tags=["Reportes"])

get_db = database.SessionLocal

def get_session():
    db = get_db()
    try:
        yield db
    finally:
        db.close()

@router.get("/dashboard")
def obtener_reporte_dashboard(db: Session = Depends(get_session)):
    """
    Obtiene métricas analíticas KPI y agrupaciones sobre citas y pacientes.
    Cumple con el nivel Bajo de Gobernanza (Reporte plano, sin datos de auditoria).
    Implementado con consultas SQL de base para mayor soporte analítico.
    """
    
    # 1. KPIs: Citas Hoy y Citas Semana 
    # (Compatibilidad con la DB por defecto SQLite, se puede migrar a Postgres)
    kpi_query = text("""
        /* Calculamos indicadores principales con funciones nativas condicionadas SQL */
        SELECT 
            SUM(CASE WHEN date(fecha) = date('now', 'localtime') THEN 1 ELSE 0 END) as citas_hoy,
            SUM(CASE WHEN date(fecha) >= date('now', '-7 days', 'localtime') THEN 1 ELSE 0 END) as citas_semana
        FROM cita;
    """)
    kpi_result = db.execute(kpi_query).fetchone()
    citas_hoy = kpi_result[0] if kpi_result and kpi_result[0] else 0
    citas_semana = kpi_result[1] if kpi_result and kpi_result[1] else 0

    # 2. Dimensión: Previsión (Atributo de cruce)
    prev_query = text("""
        /* JOIN de Hechos (Cita) y Dimension (Paciente) agrupado por la dimensión de interés */
        SELECT 
            COALESCE(p.prevision, 'Sin Registro') AS descripcion_prevision,
            COUNT(c.id) AS total_citas
        FROM cita c
        JOIN paciente p ON c.paciente_id = p.id
        GROUP BY p.prevision;
    """)
    prev_results = db.execute(prev_query).fetchall()
    
    distribucion = []
    for r in prev_results:
        distribucion.append({
            "prevision": r[0],
            "total": r[1]
        })

    return {
        "kpis": {
            "citas_hoy": citas_hoy,
            "citas_semana": citas_semana
        },
        "distribucion_prevision": distribucion
    }
