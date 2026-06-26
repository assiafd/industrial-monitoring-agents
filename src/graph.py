"""LangGraph orchestration for the industrial monitoring agents."""

from __future__ import annotations

from typing import Any

from langgraph.graph import END, StateGraph

from src.agents import EmergencyAgent, MaintenanceAgent, MonitoringAgent, RouterAgent
from src.state import WorkflowState

router_agent = RouterAgent()
maintenance_agent = MaintenanceAgent()
emergency_agent = EmergencyAgent()


def receive_telemetry(state: WorkflowState) -> WorkflowState:
    telemetry = state["telemetry"]
    monitoring = MonitoringAgent()
    monitoring.record(
        "receive_telemetry",
        "success",
        {"machine_id": telemetry.get("machine_id")},
    )
    return {**state, "monitoring": monitoring}


def route_machine_state(state: WorkflowState) -> WorkflowState:
    telemetry = state["telemetry"]
    monitoring = state["monitoring"]
    decision = router_agent.evaluate(telemetry)
    monitoring.record("route_decision", "success", decision)
    return {**state, "decision": decision}


def select_route(state: WorkflowState) -> str:
    return state["decision"]["route"]


def handle_normal_state(state: WorkflowState) -> WorkflowState:
    telemetry = state["telemetry"]
    monitoring = state["monitoring"]
    decision = state["decision"]
    result = maintenance_agent.handle(telemetry, decision)
    monitoring.record("maintenance_agent", "success", {"status": result["status"]})
    return {**state, "result": result, "final_status": "normal_traced"}


def handle_critical_state(state: WorkflowState) -> WorkflowState:
    telemetry = state["telemetry"]
    monitoring = state["monitoring"]
    decision = state["decision"]
    result = emergency_agent.handle(telemetry, decision)
    monitoring.record("emergency_agent", "success", {"status": result["status"]})
    return {**state, "result": result, "final_status": "incident_traced"}


def finalize_workflow(state: WorkflowState) -> WorkflowState:
    monitoring = state["monitoring"]
    final_status = state["final_status"]
    result = state["result"]
    monitoring.record("workflow_completed", "success", {"final_status": final_status})
    return {
        **state,
        "response": monitoring.summary(final_status=final_status, result=result),
    }


def build_workflow():
    """Build and compile the LangGraph state machine."""

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
    """Execute the compiled LangGraph workflow."""

    state = workflow.invoke({"telemetry": telemetry})
    return state["response"]
