"""FastAPI entry point and dashboard server."""

from __future__ import annotations

from pathlib import Path
<<<<<<< HEAD
from typing import Any
=======
from typing import Any, TypedDict
>>>>>>> c9a031ce3b2c32c38ee1644d82d67990a620e630

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
<<<<<<< HEAD
from pydantic import BaseModel, Field

from src.graph import run_workflow
=======
from langgraph.graph import END, StateGraph
from pydantic import BaseModel, Field

from src.agents import EmergencyAgent, MaintenanceAgent, MonitoringAgent, RouterAgent
>>>>>>> c9a031ce3b2c32c38ee1644d82d67990a620e630

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

app = FastAPI(
    title="Industrial Monitoring Agents",
    description="Système intelligent de surveillance et de maintenance industrielle.",
    version="1.0.0",
)


class TelemetryPayload(BaseModel):
    machine_id: str = Field(..., examples=["ROBOT-SOUDURE-01"])
    temperature_c: float = Field(..., ge=-50, le=200)
    vibration_mm_s: float = Field(..., ge=0)
    pressure_bar: float = Field(..., ge=0)
    energy_kw: float = Field(..., ge=0)
    rotation_rpm: float = Field(..., ge=0)
    error_code: str | None = Field(default="OK")


<<<<<<< HEAD
=======
router_agent = RouterAgent()
maintenance_agent = MaintenanceAgent()
emergency_agent = EmergencyAgent()


class WorkflowState(TypedDict, total=False):
    telemetry: dict[str, Any]
    monitoring: MonitoringAgent
    decision: dict[str, Any]
    result: dict[str, Any]
    final_status: str
    response: dict[str, Any]


def receive_telemetry(state: WorkflowState) -> WorkflowState:
    telemetry = state["telemetry"]
    monitoring = MonitoringAgent()
    monitoring.record("receive_telemetry", "success", {"machine_id": telemetry.get("machine_id")})
    return {**state, "monitoring": monitoring}


def route_machine_state(state: WorkflowState) -> WorkflowState:
    telemetry = state["telemetry"]
    monitoring = state["monitoring"]
    decision = router_agent.evaluate(telemetry)
    monitoring.record("route_decision", "success", decision)
    return {**state, "decision": decision}


def select_route(state: WorkflowState) -> str:
    return state["decision"]["route"]


def handle_critical_state(state: WorkflowState) -> WorkflowState:
    telemetry = state["telemetry"]
    monitoring = state["monitoring"]
    decision = state["decision"]
    result = emergency_agent.handle(telemetry, decision)
    monitoring.record("emergency_agent", "success", {"status": result["status"]})
    return {**state, "result": result, "final_status": "incident_traced"}


def handle_normal_state(state: WorkflowState) -> WorkflowState:
    telemetry = state["telemetry"]
    monitoring = state["monitoring"]
    decision = state["decision"]
    result = maintenance_agent.handle(telemetry, decision)
    monitoring.record("maintenance_agent", "success", {"status": result["status"]})
    return {**state, "result": result, "final_status": "normal_traced"}


def finalize_workflow(state: WorkflowState) -> WorkflowState:
    monitoring = state["monitoring"]
    final_status = state["final_status"]
    result = state["result"]
    monitoring.record("workflow_completed", "success", {"final_status": final_status})
    return {**state, "response": monitoring.summary(final_status=final_status, result=result)}


def build_workflow():
    graph = StateGraph(WorkflowState)
    graph.add_node("receive_telemetry", receive_telemetry)
    graph.add_node("route_machine_state", route_machine_state)
    graph.add_node("handle_normal_state", handle_normal_state)
    graph.add_node("handle_critical_state", handle_critical_state)
    graph.add_node("finalize_workflow", finalize_workflow)

    graph.set_entry_point("receive_telemetry")
    graph.add_edge("receive_telemetry", "route_machine_state")
    graph.add_conditional_edges(
        "route_machine_state",
        select_route,
        {
            "normal": "handle_normal_state",
            "critical": "handle_critical_state",
        },
    )
    graph.add_edge("handle_normal_state", "finalize_workflow")
    graph.add_edge("handle_critical_state", "finalize_workflow")
    graph.add_edge("finalize_workflow", END)
    return graph.compile()


workflow = build_workflow()


def run_workflow(telemetry: dict[str, Any]) -> dict[str, Any]:
    state = workflow.invoke({"telemetry": telemetry})
    return state["response"]


>>>>>>> c9a031ce3b2c32c38ee1644d82d67990a620e630
@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/analyze")
def analyze(payload: TelemetryPayload) -> dict[str, Any]:
    return run_workflow(payload.model_dump())
