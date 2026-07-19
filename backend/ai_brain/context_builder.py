import json
from datetime import datetime, timezone
from typing import Dict, Any, List

from backend.stadium_state.stadium_state import stadium_state_aggregator
from backend.event_engine.store import event_store
from backend.event_engine.models import StadiumEvent
from backend.ai_brain.interfaces import IContextBuilder
from backend.ai_brain.models import OperationalContext, SystemSummary, IncidentSummary
from backend.agents.evaluation.learning_memory import learning_memory

class ContextBuilder(IContextBuilder):
    """
    Constructs the structured JSON context for the AI Brain.
    Compresses repetitive event history and aggregates system state.
    Does NOT interact with LLMs.
    """
    def __init__(self, critical_event_limit: int = 10, warning_event_limit: int = 15):
        self.critical_event_limit = critical_event_limit
        self.warning_event_limit = warning_event_limit

    def _summarize_subsystem(self, category: str, snapshot: Dict[str, Any]) -> SystemSummary:
        """Flattens a multi-location subsystem snapshot into a single aggregated summary."""
        if category not in snapshot or not snapshot[category]:
            return SystemSummary(health="UNKNOWN", status="NO DATA", last_updated=datetime.now(timezone.utc).isoformat(), metrics={})
        
        worst_health = "GOOD"
        agg_metrics = {}
        
        for loc, state in snapshot[category].items():
            if state.health == "CRITICAL": 
                worst_health = "CRITICAL"
            elif state.health == "WARNING" and worst_health != "CRITICAL": 
                worst_health = "WARNING"
                
            if hasattr(state, 'metrics') and isinstance(state.metrics, dict):
                agg_metrics.update(state.metrics)
                
        # Take the status of the first available node as the general status text
        first_loc = list(snapshot[category].keys())[0]
        status = str(snapshot[category][first_loc].status)
        last_updated = snapshot[category][first_loc].last_updated.isoformat()
        
        return SystemSummary(
            health=worst_health,
            status=status,
            last_updated=last_updated,
            metrics=agg_metrics
        )

    def _compress_events(self, events: List[StadiumEvent]) -> List[IncidentSummary]:
        """
        Compresses raw events by grouping them by (Category, Location, Severity).
        Reduces token count while preserving the 'weight' (count) of incidents.
        """
        grouped: Dict[tuple, IncidentSummary] = {}
        for e in events:
            key = (e.category.value, e.location, e.severity.value)
            if key not in grouped:
                grouped[key] = IncidentSummary(
                    category=e.category.value,
                    severity=e.severity.value,
                    location=e.location,
                    description=e.description,
                    count=1
                )
            else:
                grouped[key].count += 1
                
        # Return sorted by count (highest frequency first)
        return sorted(list(grouped.values()), key=lambda x: x.count, reverse=True)

    def build_context(self) -> Dict[str, Any]:
        """
        Builds the unified, token-efficient JSON payload.
        """
        snapshot = stadium_state_aggregator.get_dashboard_snapshot()
        events = event_store.get_recent_events(limit=200)
        
        # Filter and compress events
        critical_events = [e for e in events if e.severity.value == "CRITICAL"]
        warning_events = [e for e in events if e.severity.value == "WARNING"]
        
        comp_critical = self._compress_events(critical_events)[:self.critical_event_limit]
        comp_warning = self._compress_events(warning_events)[:self.warning_event_limit]
        
        # Calculate Global Health
        global_health = "GOOD"
        categories = ["CROWD", "WEATHER", "MEDICAL", "GATE", "NETWORK", "IOT", "THREAT", "TICKET"]
        for cat in categories:
            summary = self._summarize_subsystem(cat, snapshot.subsystems)
            if summary.health == "CRITICAL":
                global_health = "CRITICAL"
            elif summary.health == "WARNING" and global_health != "CRITICAL":
                global_health = "WARNING"
                
        # In the schema we have 'gate' which we map to GATE or TICKET telemetry based on what's active.
        gate_summary = self._summarize_subsystem("GATE", snapshot.subsystems)
        if gate_summary.health == "UNKNOWN":
             gate_summary = self._summarize_subsystem("TICKET", snapshot.subsystems)

        ctx = OperationalContext(
            timestamp=datetime.now(timezone.utc).isoformat(),
            global_health=global_health,
            crowd=self._summarize_subsystem("CROWD", snapshot.subsystems),
            weather=self._summarize_subsystem("WEATHER", snapshot.subsystems),
            medical=self._summarize_subsystem("MEDICAL", snapshot.subsystems),
            gate=gate_summary,
            network=self._summarize_subsystem("NETWORK", snapshot.subsystems),
            iot=self._summarize_subsystem("IOT", snapshot.subsystems),
            threat=self._summarize_subsystem("THREAT", snapshot.subsystems),
            critical_incidents=comp_critical,
            recent_warnings=comp_warning
        )
        
        output_dict = ctx.model_dump(mode="json")
        output_dict["learned_lessons"] = learning_memory.get_recent_lessons()
        
        return output_dict
