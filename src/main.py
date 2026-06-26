"""FastAPI entry point and dashboard server."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from src.graph import run_workflow

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

app = FastAPI(
    title="Industrial Monitoring Agents",
    description="Système intelligent de surveillance et de maintenance industrielle.",
    version="1.1.0",
)


class TelemetryPayload(BaseModel):
    machine_id: str = Field(..., examples=["ROBOT-SOUDURE-01"])
    temperature_c: float = Field(..., ge=-50, le=200)
    vibration_mm_s: float = Field(..., ge=0)
    pressure_bar: float = Field(..., ge=0)
    energy_kw: float = Field(..., ge=0)
    rotation_rpm: float = Field(..., ge=0)
    error_code: str | None = Field(default="OK")


telemetry_history: list[dict[str, Any]] = []


def store_telemetry(payload: TelemetryPayload) -> dict[str, Any]:
    telemetry = payload.model_dump()
    analysis = run_workflow(telemetry)
    item = {
        "received_at": datetime.now(UTC).isoformat(),
        "telemetry": telemetry,
        "analysis": analysis,
    }
    telemetry_history.append(item)
    del telemetry_history[:-50]
    return item


@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/analyze")
def analyze(payload: TelemetryPayload) -> dict[str, Any]:
    return run_workflow(payload.model_dump())


@app.post("/telemetry")
def receive_machine_telemetry(payload: TelemetryPayload) -> dict[str, Any]:
    """Receive telemetry from a real machine, simulator, PLC bridge, or IoT gateway."""

    return store_telemetry(payload)


@app.get("/telemetry/latest")
def latest_machine_telemetry() -> dict[str, Any]:
    if not telemetry_history:
        return {"available": False, "message": "Aucune télémétrie reçue pour le moment."}
    return {"available": True, **telemetry_history[-1]}


@app.get("/telemetry/history")
def machine_telemetry_history() -> dict[str, Any]:
    return {"items": telemetry_history}
