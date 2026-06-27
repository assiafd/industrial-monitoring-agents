"""Monitoring agent responsible for correlation IDs and observability."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
import json
from time import perf_counter
from typing import Any
from uuid import uuid4

from src.prompts import MONITORING_PROMPT, MONITORING_SUMMARY_PROMPT
from src.utils.llm import generate_with_gemini, get_llm_metadata
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
        self.record("monitoring_agent_initialized", "success", {"prompt": MONITORING_PROMPT})

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

    def build_readable_summary_prompt(
        self,
        *,
        final_status: str,
        result: dict[str, Any],
        duration_ms: float,
        ended_at: datetime,
    ) -> str:
        execution_context = {
            "correlation_id": self.correlation_id,
            "started_at": self.started_at.isoformat(),
            "ended_at": ended_at.isoformat(),
            "duration_ms": duration_ms,
            "workflow_status": final_status,
            "events": self.events,
            "result": result,
        }
        return MONITORING_SUMMARY_PROMPT.format(
            execution_context=json.dumps(execution_context, ensure_ascii=False, indent=2, default=str)
        )

    def build_readable_summary(
        self,
        *,
        final_status: str,
        result: dict[str, Any],
        duration_ms: float,
        ended_at: datetime,
    ) -> dict[str, Any]:
        """Generate an operator-friendly summary while preserving deterministic logs."""

        prompt = self.build_readable_summary_prompt(
            final_status=final_status,
            result=result,
            duration_ms=duration_ms,
            ended_at=ended_at,
        )
        llm_response = generate_with_gemini(prompt)
        fallback_text = (
            f"Exécution {self.correlation_id} terminée avec le statut {final_status} "
            f"en {duration_ms} ms. Résultat principal: {result.get('status', 'unknown')}."
        )
        return {
            "agent_prompt": prompt,
            "llm": {
                **get_llm_metadata(),
                "response": llm_response,
            },
            "text": llm_response.get("text") or fallback_text,
        }

    def summary(self, final_status: str, result: dict[str, Any]) -> dict[str, Any]:
        """Return a compact execution summary for API responses."""

        ended_at = datetime.now(UTC)
        duration_ms = round((perf_counter() - self._start_timer) * 1000, 2)
        readable_summary = self.build_readable_summary(
            final_status=final_status,
            result=result,
            duration_ms=duration_ms,
            ended_at=ended_at,
        )
        return {
            "correlation_id": self.correlation_id,
            "started_at": self.started_at.isoformat(),
            "ended_at": ended_at.isoformat(),
            "duration_ms": duration_ms,
            "workflow_status": final_status,
            "events": self.events,
            "monitoring_summary": readable_summary,
            "result": result,
        }
