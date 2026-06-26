from src.agents.router import RouterAgent


def test_router_returns_normal_route_for_safe_telemetry():
    telemetry = {
        "machine_id": "CNC-01",
        "temperature_c": 62,
        "vibration_mm_s": 2.1,
        "pressure_bar": 8,
        "energy_kw": 21,
        "rotation_rpm": 1500,
        "error_code": "OK",
    }

    decision = RouterAgent().evaluate(telemetry)

    assert decision["route"] == "normal"
    assert decision["severity"] == "low"
    assert decision["issues"] == []


def test_router_returns_critical_route_for_dangerous_telemetry():
    telemetry = {
        "machine_id": "PRESS-01",
        "temperature_c": 95,
        "vibration_mm_s": 9.2,
        "pressure_bar": 14,
        "energy_kw": 30,
        "rotation_rpm": 1800,
        "error_code": "OK",
    }

    decision = RouterAgent().evaluate(telemetry)

    assert decision["route"] == "critical"
    assert decision["severity"] == "high"
    assert "Température excessive" in decision["issues"]
    assert "Vibrations anormales" in decision["issues"]
