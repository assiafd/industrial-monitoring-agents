"""Agent for the normal preventive-maintenance route."""

from __future__ import annotations

<<<<<<< HEAD
import json
from typing import Any

from src.prompts import MAINTENANCE_PROMPT


class MaintenanceAgent:
    """Prompt-driven agent for the preventive-maintenance route."""

    def build_prompt(self, telemetry: dict[str, Any], decision: dict[str, Any]) -> str:
        return MAINTENANCE_PROMPT.format(
            decision=json.dumps(decision, ensure_ascii=False, indent=2, default=str),
            telemetry=json.dumps(telemetry, ensure_ascii=False, indent=2),
        )
=======
from typing import Any


class MaintenanceAgent:
    """Produces recommendations when the machine operates normally."""
>>>>>>> c9a031ce3b2c32c38ee1644d82d67990a620e630

    def handle(self, telemetry: dict[str, Any], decision: dict[str, Any]) -> dict[str, Any]:
        machine_id = decision["machine_id"]
        return {
            "status": "normal",
            "machine_id": machine_id,
<<<<<<< HEAD
            "agent_prompt": self.build_prompt(telemetry, decision),
=======
>>>>>>> c9a031ce3b2c32c38ee1644d82d67990a620e630
            "message": "La machine fonctionne correctement.",
            "diagnostic": "Aucun indicateur critique détecté sur la télémétrie reçue.",
            "actions": [
                "Continuer la surveillance en temps réel",
                "Conserver les mesures dans les journaux d'observabilité",
                "Planifier la maintenance préventive selon le calendrier standard",
            ],
            "telemetry_snapshot": telemetry,
        }
