"""Decision agent that routes telemetry to normal or critical handling."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Thresholds:
    max_temperature_c: float = 85.0
    max_vibration_mm_s: float = 7.5
    max_pressure_bar: float = 12.0
    max_energy_kw: float = 45.0
    min_rotation_rpm: float = 500.0
    max_rotation_rpm: float = 3500.0


class RouterAgent:
    """Evaluates machine telemetry and chooses a workflow route."""

    def __init__(self, thresholds: Thresholds | None = None) -> None:
        self.thresholds = thresholds or Thresholds()

    def evaluate(self, telemetry: dict[str, Any]) -> dict[str, Any]:
        issues: list[str] = []

        temperature = float(telemetry.get("temperature_c", 0))
        vibration = float(telemetry.get("vibration_mm_s", 0))
        pressure = float(telemetry.get("pressure_bar", 0))
        energy = float(telemetry.get("energy_kw", 0))
        rotation = float(telemetry.get("rotation_rpm", 0))
        error_code = telemetry.get("error_code")

        if temperature > self.thresholds.max_temperature_c:
            issues.append("Température excessive")
        if vibration > self.thresholds.max_vibration_mm_s:
            issues.append("Vibrations anormales")
        if pressure > self.thresholds.max_pressure_bar:
            issues.append("Pression élevée")
        if energy > self.thresholds.max_energy_kw:
            issues.append("Consommation électrique élevée")
        if rotation < self.thresholds.min_rotation_rpm or rotation > self.thresholds.max_rotation_rpm:
            issues.append("Vitesse de rotation hors plage")
        if error_code not in (None, "", "OK", "NONE"):
            issues.append(f"Code erreur détecté: {error_code}")

        route = "critical" if issues else "normal"
        severity = "high" if len(issues) >= 2 else "medium" if issues else "low"

        return {
            "route": route,
            "severity": severity,
            "issues": issues,
            "machine_id": telemetry.get("machine_id", "unknown"),
        }
