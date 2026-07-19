import threading
from pydantic import BaseModel
from datetime import datetime, timezone
from typing import Dict, Any, List
from backend.event_engine.models import StadiumEvent
from backend.event_engine.event_bus import event_bus, Subscriber

class SubsystemState(BaseModel):
    category: str
    status: str
    health: str
    severity: str
    last_updated: datetime
    metrics: Dict[str, Any]

class GlobalStadiumSnapshot(BaseModel):
    timestamp: datetime
    subsystems: Dict[str, Dict[str, SubsystemState]]

class StadiumStateAggregator(Subscriber):
    """
    Centralized StadiumState Aggregator.
    Maintains the real-time health of every subsystem in a thread-safe manner.
    """
    def __init__(self):
        self._lock = threading.Lock()
        # Dictionary structure: category -> location/source -> SubsystemState
        self._state: Dict[str, Dict[str, SubsystemState]] = {}
        # Subscribe to all events
        event_bus.subscribe(self, topic=None)
        
    def update(self, event: StadiumEvent) -> None:
        """Subscriber interface implementation."""
        self.update_state(event)
        
    def _calculate_health(self, severity: str) -> str:
        if severity == "CRITICAL":
            return "Critical"
        elif severity == "WARNING":
            return "Degraded"
        return "Good"
        
    def update_state(self, event: StadiumEvent) -> None:
        """Thread-safe method to update internal state from an incoming StadiumEvent."""
        with self._lock:
            category_key = event.category.value
            state_key = event.location if event.location else event.source
            
            if category_key not in self._state:
                self._state[category_key] = {}
                
            self._state[category_key][state_key] = SubsystemState(
                category=category_key,
                status="Active",
                health=self._calculate_health(event.severity.value),
                severity=event.severity.value,
                last_updated=event.timestamp,
                metrics=event.metrics
            )
            
    def get_current_state(self) -> GlobalStadiumSnapshot:
        """
        Returns the full Pydantic snapshot.
        Ideal for deep AI reasoning (e.g., AI Brain) where schema validation is critical.
        """
        with self._lock:
            # Build a safe deep copy using Pydantic methods
            subsystems_copy = {}
            for cat, locs in self._state.items():
                subsystems_copy[cat] = {}
                for loc, state in locs.items():
                    # Support Pydantic v1 (copy) and v2 (model_copy)
                    copy_method = getattr(state, 'model_copy', state.copy)
                    subsystems_copy[cat][loc] = copy_method()
                    
            return GlobalStadiumSnapshot(
                timestamp=datetime.now(timezone.utc),
                subsystems=subsystems_copy
            )
            
    def get_dashboard_snapshot(self) -> Dict[str, Any]:
        """
        Returns a flattened, lightweight dictionary.
        Optimized for UI rendering or simple JSON responses.
        """
        snapshot = self.get_current_state()
        if hasattr(snapshot, 'model_dump'):
            return snapshot.model_dump()
        return snapshot.dict()
        
    def get_operational_summary(self) -> str:
        """
        Returns a human-readable string summarizing degraded/critical systems.
        Perfect for injecting concise context into a Copilot prompt.
        """
        summary = []
        with self._lock:
            for cat, locs in self._state.items():
                for loc, state in locs.items():
                    if state.health in ["Critical", "Degraded"]:
                        summary.append(f"[{cat}] {loc}: {state.health} (Severity: {state.severity}) - Last Updated: {state.last_updated.isoformat()}")
        
        if not summary:
            return "All subsystems operating normally. No active threats or degradation."
        return "\n".join(summary)

# Global Aggregator Instance
stadium_state_aggregator = StadiumStateAggregator()
