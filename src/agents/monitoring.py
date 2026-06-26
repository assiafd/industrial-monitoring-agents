"""Monitoring agent responsible for correlation IDs and observability."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from time import perf_counter
from typing import Any
from uuid import uuid4

from src.utils.logger import configure_logger


@dataclass
class MonitoringAgent:
    """Collects trace data for one workflow execution."""

    correlation_id: str = field(default_factory=lambda: str(uuid4()))
    started_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    events: list[dict[str, Any]] = field(default_factory=list)

    def __post_init__(self) -> None:
        self._logger = configure_logger()
        self._start_timer = perf_counter()

    def record(self, step: str, status: str, details: dict[str, Any] | None = None) -> None:
        """Append an observable workflow event and write a structured log."""

        event = {
            "correlation_id": self.correlation_id,
            "timestamp": datetime.now(UTC).isoformat(),
            "step": step,
            "status": status,
            "details": details or {},
        }
        self.events.append(event)
        self._logger.info(
            "workflow_event",
            extra={
                "correlation_id": self.correlation_id,
                "step": step,
                "status": status,
                "details": details or {},
            },
        )

    def summary(self, final_status: str, result: dict[str, Any]) -> dict[str, Any]:
        """Return a compact execution summary for API responses."""

        ended_at = datetime.now(UTC)
        duration_ms = round((perf_counter() - self._start_timer) * 1000, 2)
        return {
            "correlation_id": self.correlation_id,
            "started_at": self.started_at.isoformat(),
            "ended_at": ended_at.isoformat(),
            "duration_ms": duration_ms,
            "workflow_status": final_status,
            "events": self.events,
            "result": result,
        }
