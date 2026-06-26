"""Agent for the critical emergency and safety route."""

from __future__ import annotations

import json
from typing import Any

from src.prompts import EMERGENCY_PROMPT
from src.utils.slack import send_critical_incident_report


class EmergencyAgent:
    """Prompt-driven agent for the emergency and safety route."""

    def build_prompt(self, telemetry: dict[str, Any], decision: dict[str, Any]) -> str:
        return EMERGENCY_PROMPT.format(
            decision=json.dumps(decision, ensure_ascii=False, indent=2, default=str),
            telemetry=json.dumps(telemetry, ensure_ascii=False, indent=2),
        )

    def handle(
        self,
        telemetry: dict[str, Any],
        decision: dict[str, Any],
        correlation_id: str | None = None,
    ) -> dict[str, Any]:
        machine_id = decision["machine_id"]
        issues = decision["issues"]
        diagnostic = " ; ".join(issues) if issues else "Anomalie critique non qualifiée."
        actions = [
            "Notifier immédiatement l'équipe de maintenance",
            "Sécuriser la zone et préparer l'arrêt contrôlé si nécessaire",
            "Inspecter les composants liés aux anomalies détectées",
            "Conserver le Correlation ID pour l'analyse post-incident",
        ]
        slack_notification = send_critical_incident_report(
            telemetry=telemetry,
            diagnostic=diagnostic,
            actions=actions,
            correlation_id=correlation_id,
        )
        return {
            "status": "critical",
            "machine_id": machine_id,
            "agent_prompt": self.build_prompt(telemetry, decision),
            "message": "Incident critique détecté.",
            "diagnostic": diagnostic,
            "actions": actions,
            "slack_notification": slack_notification,
            "telemetry_snapshot": telemetry,
        }
