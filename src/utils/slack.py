"""Slack notification helpers for critical incidents."""

from __future__ import annotations

import os
from typing import Any

import requests


SLACK_API_URL = "https://slack.com/api"


def _resolve_channel_id(token: str, channel_name: str) -> str:
    """Return a Slack channel ID from a channel ID or a public/private channel name."""

    normalized_name = channel_name.lstrip("#")
    if normalized_name.startswith(("C", "G", "D")):
        return normalized_name

    cursor: str | None = None
    headers = {"Authorization": f"Bearer {token}"}

    while True:
        params = {
            "limit": 200,
            "types": "public_channel,private_channel",
        }
        if cursor:
            params["cursor"] = cursor

        response = requests.get(
            f"{SLACK_API_URL}/conversations.list",
            headers=headers,
            params=params,
            timeout=10,
        )
        response.raise_for_status()
        payload = response.json()
        if not payload.get("ok"):
            raise RuntimeError(payload.get("error", "slack_conversations_list_failed"))

        for channel in payload.get("channels", []):
            if channel.get("name") == normalized_name:
                return channel["id"]

        cursor = payload.get("response_metadata", {}).get("next_cursor")
        if not cursor:
            break

    raise RuntimeError(f"Slack channel not found: {channel_name}")


def send_critical_incident_report(
    *,
    telemetry: dict[str, Any],
    diagnostic: str,
    actions: list[str],
    correlation_id: str | None,
) -> dict[str, Any]:
    """Send a critical incident report to Slack when Slack env vars are configured."""

    token = (os.getenv("SLACK_BOT_TOKEN") or "").strip()
    channel_name = (os.getenv("SLACK_CHANNEL_NAME", "nouveau-canal") or "nouveau-canal").strip()

    if not token:
        return {
            "status": "skipped",
            "reason": "SLACK_BOT_TOKEN is not configured",
            "channel": channel_name,
        }

    try:
        channel_id = _resolve_channel_id(token, channel_name)
        actions_text = "\n".join(f"• {action}" for action in actions)
        message = (
            ":rotating_light: *Incident critique détecté*\n"
            f"*Machine* : {telemetry.get('machine_id', 'unknown')}\n"
            f"*Correlation ID* : `{correlation_id or 'non disponible'}`\n"
            f"*Diagnostic* : {diagnostic}\n"
            "*Télémétrie* : "
            f"temp={telemetry.get('temperature_c')}°C, "
            f"vibration={telemetry.get('vibration_mm_s')} mm/s, "
            f"pression={telemetry.get('pressure_bar')} bar, "
            f"énergie={telemetry.get('energy_kw')} kW, "
            f"rotation={telemetry.get('rotation_rpm')} rpm, "
            f"code={telemetry.get('error_code') or 'OK'}\n"
            f"*Actions recommandées* :\n{actions_text}"
        )

        response = requests.post(
            f"{SLACK_API_URL}/chat.postMessage",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json; charset=utf-8",
            },
            json={
                "channel": channel_id,
                "text": message,
            },
            timeout=10,
        )
        response.raise_for_status()
        payload = response.json()
        if not payload.get("ok"):
            raise RuntimeError(payload.get("error", "slack_post_message_failed"))

        return {
            "status": "sent",
            "channel": channel_name,
            "channel_id": channel_id,
            "timestamp": payload.get("ts"),
        }
    except Exception as exc:
        return {
            "status": "failed",
            "channel": channel_name,
            "error": str(exc),
        }
