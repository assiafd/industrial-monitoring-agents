"""Agent for the critical emergency and safety route."""

from __future__ import annotations

from typing import Any


class EmergencyAgent:
    """Produces an incident diagnosis and emergency actions."""

    def handle(self, telemetry: dict[str, Any], decision: dict[str, Any]) -> dict[str, Any]:
        machine_id = decision["machine_id"]
        issues = decision["issues"]
        return {
            "status": "critical",
            "machine_id": machine_id,
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
