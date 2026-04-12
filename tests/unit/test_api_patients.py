from fastapi.testclient import TestClient
from src.backend.main import app

client = TestClient(app)
# Forzamos temporalmente la IP a 127.0.0.1 para que el middleware no bloquee los requests de la suite
client.base_url = "http://testserver"

def test_health_check():
    # Simulamos ip de cliente
    res = client.get("/", headers={"X-Forwarded-For": "127.0.0.1"})
    assert res.status_code == 200

def test_create_and_get_patient():
    patient_data = {
        "rut": "12345678-9",
        "nombres": "Juan",
        "apellidos": "Perez",
        "fecha_nacimiento": "1990-01-01",
        "sexo": "M",
        "correo": "juan@ejemplo.com",
        "telefono": "+56912345678",
        "prevision": "fonasa"
    }

    # Test Create (POST)
    response = client.post("/patients/", json=patient_data)
    assert response.status_code == 201
    data = response.json()
    assert data["rut"] == "12345678-9"
    assert "patient_id" in data

    # Test Invalid Format RUT
    bad_rut_data = patient_data.copy()
    bad_rut_data["rut"] = "1234abcd"
    bad_res = client.post("/patients/", json=bad_rut_data)
    assert bad_res.status_code == 422 # Fallo de validación Pydantic

    # Test Read (GET)
    get_res = client.get("/patients/12345678-9")
    assert get_res.status_code == 200
    assert get_res.json()["apellidos"] == "Perez"

def test_update_patient():
    update_data = {
        "telefono": "+56900000000",
        "prevision": "isapre"
    }
    response = client.put("/patients/12345678-9", json=update_data)
    assert response.status_code == 200
    assert response.json()["telefono"] == "+56900000000"
    assert response.json()["prevision"] == "isapre"

def test_delete_patient():
    delete_res = client.delete("/patients/12345678-9")
    assert delete_res.status_code == 204

    # Verificar que ya no existe
    get_res = client.get("/patients/12345678-9")
    assert get_res.status_code == 404
