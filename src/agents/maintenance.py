"""Agent for the normal preventive-maintenance route."""

from __future__ import annotations

from typing import Any


class MaintenanceAgent:
    """Produces recommendations when the machine operates normally."""

    def handle(self, telemetry: dict[str, Any], decision: dict[str, Any]) -> dict[str, Any]:
        machine_id = decision["machine_id"]
        return {
            "status": "normal",
            "machine_id": machine_id,
            "message": "La machine fonctionne correctement.",
            "diagnostic": "Aucun indicateur critique détecté sur la télémétrie reçue.",
            "actions": [
                "Continuer la surveillance en temps réel",
                "Conserver les mesures dans les journaux d'observabilité",
                "Planifier la maintenance préventive selon le calendrier standard",
            ],
            "telemetry_snapshot": telemetry,
        }
