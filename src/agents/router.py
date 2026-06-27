"""Decision agent that routes telemetry to normal or critical handling."""

from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any

from src.prompts import ROUTER_PROMPT
from src.utils.llm import generate_with_gemini, get_llm_metadata
from src.utils.ml_model import predict_machine_health


@dataclass(frozen=True)
class Thresholds:
    max_temperature_c: float = 85.0
    max_vibration_mm_s: float = 7.5
    max_pressure_bar: float = 12.0
    max_energy_kw: float = 45.0
    min_rotation_rpm: float = 500.0
    max_rotation_rpm: float = 3500.0


class RouterAgent:
    """Prompt-driven agent that chooses the normal or critical route."""

    def __init__(self, thresholds: Thresholds | None = None) -> None:
        self.thresholds = thresholds or Thresholds()

    def build_prompt(self, telemetry: dict[str, Any]) -> str:
        return ROUTER_PROMPT.format(
            max_temperature_c=self.thresholds.max_temperature_c,
            max_vibration_mm_s=self.thresholds.max_vibration_mm_s,
            max_pressure_bar=self.thresholds.max_pressure_bar,
            max_energy_kw=self.thresholds.max_energy_kw,
            min_rotation_rpm=self.thresholds.min_rotation_rpm,
            max_rotation_rpm=self.thresholds.max_rotation_rpm,
            telemetry=json.dumps(telemetry, ensure_ascii=False, indent=2),
        )

    def evaluate(self, telemetry: dict[str, Any]) -> dict[str, Any]:
        issues: list[str] = []
        prompt = self.build_prompt(telemetry)
        llm_analysis = generate_with_gemini(prompt)
        ml_prediction = predict_machine_health(telemetry)

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

        if route == "normal" and ml_prediction.get("label") == "critical":
            route = "critical"
            severity = "medium"
            issues.append("Prédiction ML critique")

        return {
            "route": route,
            "severity": severity,
            "issues": issues,
            "ml_prediction": ml_prediction,
            "machine_id": telemetry.get("machine_id", "unknown"),
            "prompt": prompt,
            "llm": {
                **get_llm_metadata(),
                "response": llm_analysis,
            },
            "reasoning": (
                "Route critique sélectionnée car au moins une anomalie dépasse les seuils."
                if issues
                else "Route normale sélectionnée car toutes les mesures sont dans les seuils."
            ),
        }
