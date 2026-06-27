"""Agent for the normal preventive-maintenance route."""

from __future__ import annotations

import json
from typing import Any

from src.prompts import MAINTENANCE_PROMPT
from src.utils.llm import generate_with_gemini, get_llm_metadata


class MaintenanceAgent:
    """Prompt-driven agent for the preventive-maintenance route."""

    def build_prompt(self, telemetry: dict[str, Any], decision: dict[str, Any]) -> str:
        return MAINTENANCE_PROMPT.format(
            decision=json.dumps(decision, ensure_ascii=False, indent=2, default=str),
            telemetry=json.dumps(telemetry, ensure_ascii=False, indent=2),
        )

    def handle(self, telemetry: dict[str, Any], decision: dict[str, Any]) -> dict[str, Any]:
        machine_id = decision["machine_id"]
        prompt = self.build_prompt(telemetry, decision)
        llm_analysis = generate_with_gemini(prompt)
        return {
            "status": "normal",
            "machine_id": machine_id,
            "agent_prompt": prompt,
            "llm": {
                **get_llm_metadata(),
                "response": llm_analysis,
            },
            "message": "La machine fonctionne correctement.",
            "diagnostic": "Aucun indicateur critique détecté sur la télémétrie reçue.",
            "actions": [
                "Continuer la surveillance en temps réel",
                "Conserver les mesures dans les journaux d'observabilité",
                "Planifier la maintenance préventive selon le calendrier standard",
            ],
            "telemetry_snapshot": telemetry,
        }
