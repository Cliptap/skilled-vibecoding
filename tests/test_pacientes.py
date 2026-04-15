from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_create_and_get_paciente():
    paciente = {
        "nombre": "Juan",
        "apellido": "Pérez",
        "rut": "12345678-9",
        "telefono": "123456789",
        "correo": "juan@example.com",
        "sexo": "M",
        "fecha_nacimiento": "1990-01-01",
        "prevision": "Fonasa"
    }
    response = client.post("/pacientes/", json=paciente)
    assert response.status_code == 201
    data = response.json()
    assert data["nombre"] == "Juan"
    paciente_id = data["id"]

    # Get paciente
    response = client.get(f"/pacientes/{paciente_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["rut"] == "12345678-9"

def test_buscar_paciente_por_rut():
    rut = "12345678-9"
    response = client.get(f"/pacientes/buscar/{rut}")
    assert response.status_code == 200
    data = response.json()
    assert data["rut"] == rut
