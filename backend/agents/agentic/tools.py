from typing import Dict, Any, List
from backend.stadium_state.stadium_state import stadium_state_aggregator
from backend.event_engine.store import event_store
from backend.event_engine.models import StadiumEvent, EventCategory, SeverityLevel
import datetime
import uuid

def _now() -> str:
    return datetime.datetime.utcnow().isoformat()

def allocate_security(sector: str, personnel_count: int) -> Dict[str, Any]:
    """Mock tool to allocate security personnel."""
    evt = StadiumEvent(
        event_id=f"OP-{uuid.uuid4().hex[:6]}",
        timestamp=_now(),
        category=EventCategory.SECURITY,
        severity=SeverityLevel.INFO,
        source="Agentic-Ops",
        location=sector,
        description=f"Allocated {personnel_count} security personnel to {sector}.",
        raw_payload={"personnel_count": personnel_count}
    )
    event_store.add_event(evt)
    return {"status": "SUCCESS", "action": "allocate_security", "sector": sector, "count": personnel_count}

def open_gate(gate_id: str) -> Dict[str, Any]:
    """Mock tool to open a gate."""
    stadium_state_aggregator.update_subsystem("GATE", gate_id, "GOOD", "Open - Flowing")
    return {"status": "SUCCESS", "action": "open_gate", "gate_id": gate_id}

def close_gate(gate_id: str) -> Dict[str, Any]:
    """Mock tool to close a gate."""
    stadium_state_aggregator.update_subsystem("GATE", gate_id, "CRITICAL", "Closed - Locked")
    return {"status": "SUCCESS", "action": "close_gate", "gate_id": gate_id}

def notify_staff(department: str, message: str) -> Dict[str, Any]:
    """Mock tool to send notification to staff devices."""
    evt = StadiumEvent(
        event_id=f"OP-{uuid.uuid4().hex[:6]}",
        timestamp=_now(),
        category=EventCategory.SYSTEM,
        severity=SeverityLevel.INFO,
        source="Agentic-Ops",
        location="Stadium-Wide",
        description=f"Notification to {department}: {message}",
        raw_payload={"department": department, "message": message}
    )
    event_store.add_event(evt)
    return {"status": "SUCCESS", "action": "notify_staff", "department": department}

def update_signage(location: str, message: str) -> Dict[str, Any]:
    """Mock tool to update digital signage."""
    return {"status": "SUCCESS", "action": "update_signage", "location": location, "message": message}

def log_operation(message: str) -> Dict[str, Any]:
    """Logs a general operational memo."""
    return {"status": "SUCCESS", "action": "log_operation", "message": message}

# The Registry maps string tool names to the actual python functions
TOOL_REGISTRY = {
    "allocate_security": allocate_security,
    "open_gate": open_gate,
    "close_gate": close_gate,
    "notify_staff": notify_staff,
    "update_signage": update_signage,
    "log_operation": log_operation
}
