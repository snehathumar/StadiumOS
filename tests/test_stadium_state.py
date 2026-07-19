import pytest
from datetime import datetime, timezone
from backend.stadium_state.stadium_state import StadiumStateAggregator, SubsystemState
from backend.event_engine.models import StadiumEvent, EventCategory, Severity, Priority

@pytest.fixture
def state_aggregator():
    return StadiumStateAggregator()

def test_update_from_event(state_aggregator):
    event = StadiumEvent(
        category=EventCategory.GATE,
        severity=Severity.CRITICAL,
        priority=Priority.HIGH,
        source="Gate B Sensor",
        location="Gate B",
        description="Gate is blocked",
        metrics={"flow_rate": 0}
    )
    
    state_aggregator.update(event)
    
    # Internal state is _state
    assert "GATE" in state_aggregator._state
    assert "Gate B" in state_aggregator._state["GATE"]
    
    state = state_aggregator._state["GATE"]["Gate B"]
    assert state.health == "Critical"
    assert state.severity == "CRITICAL"
    assert state.metrics == {"flow_rate": 0}

def test_get_current_state(state_aggregator):
    event = StadiumEvent(
        category=EventCategory.WEATHER,
        severity=Severity.INFO,
        priority=Priority.LOW,
        source="Stadium Sensor",
        location="Stadium",
        description="Clear skies",
        metrics={"temp": 22}
    )
    state_aggregator.update(event)
    
    snapshot = state_aggregator.get_current_state()
    assert "WEATHER" in snapshot.subsystems
    assert "Stadium" in snapshot.subsystems["WEATHER"]
    assert snapshot.subsystems["WEATHER"]["Stadium"].health == "Good"
