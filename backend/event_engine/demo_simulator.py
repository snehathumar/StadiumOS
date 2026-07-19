import time
import datetime
import uuid
from typing import Dict, Any

from backend.event_engine.models import StadiumEvent, Severity, EventCategory, Priority
from backend.event_engine.store import event_store
from backend.stadium_state.stadium_state import stadium_state_aggregator

class DemoSimulator:
    """
    Injects deterministic scenarios into StadiumOS for Copilot UI demonstration.
    Overrides live telemetry with hardcoded crisis states.
    """
    
    @staticmethod
    def _now() -> str:
        return datetime.datetime.utcnow().isoformat()

    @staticmethod
    def update_subsystem(category: str, location: str, health: str, status: str, metrics: Dict[str, Any]):
        evt = StadiumEvent(
            source=location,
            location=location,
            category=EventCategory(category),
            severity=Severity.CRITICAL if health == "CRITICAL" else Severity.WARNING,
            priority=Priority.HIGH if health == "CRITICAL" else Priority.MEDIUM,
            description=status,
            metrics=metrics
        )
        stadium_state_aggregator.update(evt)

    @staticmethod
    def inject_scenario_1_overcrowding():
        """Simulates Gate A Overcrowding."""
        # 1. Update global state directly
        DemoSimulator.update_subsystem("GATE", "Gate A", "CRITICAL", "Overcrowded", {
            "occupancy": 92,
            "queue_length": 850,
            "wait_time_mins": 18
        })
        DemoSimulator.update_subsystem("GATE", "Gate B", "GOOD", "Clear", {
            "occupancy": 35,
            "queue_length": 50,
            "wait_time_mins": 2
        })
        
        # 2. Inject noisy events
        for _ in range(5):
            evt = StadiumEvent(
                timestamp=DemoSimulator._now(),
                category=EventCategory.CROWD,
                severity=Severity.WARNING,
                priority=Priority.MEDIUM,
                source="Camera-G12",
                location="Gate A",
                description="High density detected at Gate A entrance.",
                metrics={"density": 0.85}
            )
            event_store.add_event(evt)
            
    @staticmethod
    def inject_scenario_2_security_threat():
        """Simulates an active security threat at Sector C."""
        DemoSimulator.update_subsystem("SECURITY", "Sector C", "CRITICAL", "Active Incident", {
            "threat_type": "Unauthorized Access",
            "confidence": 0.95,
            "security_personnel_nearby": 2
        })
        
        evt = StadiumEvent(
            timestamp=DemoSimulator._now(),
            category=EventCategory.SECURITY,
            severity=Severity.CRITICAL,
            priority=Priority.HIGH,
            source="Turnstile-C3",
            location="Sector C",
            description="Multiple forced entry attempts detected. Barrier breached.",
            metrics={"breach": True, "count": 4}
        )
        event_store.add_event(evt)

    @staticmethod
    def inject_scenario_3_predictive_simulation():
        """Simulates a predictive pattern (post-match egress surge)."""
        DemoSimulator.update_subsystem("CROWD", "Stadium Bowl", "WARNING", "Egress Surge Imminent", {
            "match_status": "90th Minute",
            "current_bowl_occupancy": 55000,
            "predicted_corridor_density_in_5m": 0.98
        })
        
        evt = StadiumEvent(
            timestamp=DemoSimulator._now(),
            category=EventCategory.SYSTEM,
            severity=Severity.INFO,
            priority=Priority.LOW,
            source="Predictive-Engine",
            location="Stadium-Wide",
            description="Predictive model anticipates massive egress surge towards North and East transit hubs.",
            metrics={"prediction_confidence": 0.99, "target_hubs": ["North", "East"]}
        )
        event_store.add_event(evt)
        
    @staticmethod
    def reset():
        """Clears events (state reset is harder, but this suffices for demo)."""
        event_store.clear()
        
demo_simulator = DemoSimulator()
