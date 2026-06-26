"""Agent for the critical emergency and safety route."""

from __future__ import annotations

<<<<<<< HEAD
import json
from typing import Any

from src.prompts import EMERGENCY_PROMPT


class EmergencyAgent:
    """Prompt-driven agent for the emergency and safety route."""

    def build_prompt(self, telemetry: dict[str, Any], decision: dict[str, Any]) -> str:
        return EMERGENCY_PROMPT.format(
            decision=json.dumps(decision, ensure_ascii=False, indent=2, default=str),
            telemetry=json.dumps(telemetry, ensure_ascii=False, indent=2),
        )
=======
from typing import Any


class EmergencyAgent:
    """Produces an incident diagnosis and emergency actions."""
>>>>>>> c9a031ce3b2c32c38ee1644d82d67990a620e630

    def handle(self, telemetry: dict[str, Any], decision: dict[str, Any]) -> dict[str, Any]:
        machine_id = decision["machine_id"]
        issues = decision["issues"]
        return {
            "status": "critical",
            "machine_id": machine_id,
<<<<<<< HEAD
            "agent_prompt": self.build_prompt(telemetry, decision),
=======
>>>>>>> c9a031ce3b2c32c38ee1644d82d67990a620e630
            "message": "Incident critique détecté.",
            "diagnostic": " ; ".join(issues) if issues else "Anomalie critique non qualifiée.",
            "actions": [
                "Notifier immédiatement l'équipe de maintenance",
                "Sécuriser la zone et préparer l'arrêt contrôlé si nécessaire",
                "Inspecter les composants liés aux anomalies détectées",
                "Conserver le Correlation ID pour l'analyse post-incident",
            ],
            "telemetry_snapshot": telemetry,
        }
