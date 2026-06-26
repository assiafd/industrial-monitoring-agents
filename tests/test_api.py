from fastapi.testclient import TestClient

from src.main import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_analyze_endpoint_returns_correlation_id_for_normal_route():
    payload = {
        "machine_id": "ROBOT-SOUDURE-01",
        "temperature_c": 70,
        "vibration_mm_s": 3.4,
        "pressure_bar": 9,
        "energy_kw": 26,
        "rotation_rpm": 1800,
        "error_code": "OK",
    }

    response = client.post("/analyze", json=payload)
    body = response.json()

    assert response.status_code == 200
    assert body["correlation_id"]
    assert body["workflow_status"] == "normal_traced"
    assert body["result"]["status"] == "normal"
    assert "agent_prompt" in body["result"]
    assert "correlation_id" in body["events"][0]


def test_analyze_endpoint_routes_critical_incident():
    payload = {
        "machine_id": "PRESS-HYDRAULIQUE-02",
        "temperature_c": 96,
        "vibration_mm_s": 9.1,
        "pressure_bar": 13,
        "energy_kw": 30,
        "rotation_rpm": 1800,
        "error_code": "E_TEMP",
    }

    response = client.post("/analyze", json=payload)
    body = response.json()

    assert response.status_code == 200
    assert body["workflow_status"] == "incident_traced"
    assert body["result"]["status"] == "critical"
    assert "Tu es EmergencyAgent" in body["result"]["agent_prompt"]
