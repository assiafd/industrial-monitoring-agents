"""Shared LangGraph state for the monitoring workflow."""

from __future__ import annotations

from typing import Any, TypedDict

from src.agents.monitoring import MonitoringAgent


class WorkflowState(TypedDict, total=False):
    """State passed between LangGraph nodes."""

    telemetry: dict[str, Any]
    monitoring: MonitoringAgent
    decision: dict[str, Any]
    result: dict[str, Any]
    final_status: str
    response: dict[str, Any]
