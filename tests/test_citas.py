from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_create_and_get_cita():
    # Crear paciente primero
    paciente = {
        "nombre": "Ana",
        "apellido": "Gómez",
        "rut": "98765432-1",
        "telefono": "987654321",
        "correo": "ana@example.com",
        "sexo": "F",
        "fecha_nacimiento": "1985-05-05",
        "prevision": "Isapre"
    }
    resp_paciente = client.post("/pacientes/", json=paciente)
    paciente_id = resp_paciente.json()["id"]

    cita = {
        "paciente_id": paciente_id,
        "fecha": "2026-04-12T10:00:00+00:00",
        "razon": "Control"
    }
    response = client.post("/citas/", json=cita)
    assert response.status_code == 201
    data = response.json()
    assert data["razon"] == "Control"
    cita_id = data["id"]

    # Get cita
    response = client.get(f"/citas/{cita_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["paciente_id"] == paciente_id

    # Listar por fecha
    response = client.get("/citas/por_fecha/2026-04-12")
    assert response.status_code == 200
    citas = response.json()
    assert any(cita["razon"] == "Control" for cita in citas)
