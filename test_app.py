import pytest
import sys
from unittest.mock import MagicMock
from backend.event_engine.models import StadiumEvent, EventCategory, Severity, Priority
from backend.stadium_state.stadium_state import StadiumStateAggregator
from backend.ai_brain.models import StadiumBrainResponse
from backend.ai_brain.ai_manager import AIManager, IAIProvider
import json

# Mock Google Generative AI to prevent test failures on missing keys/dependencies
sys.modules['google.generativeai'] = MagicMock()

class MockAIProvider(IAIProvider):
    def generate_response(self, system_prompt: str, user_prompt: str) -> str:
        return json.dumps({
            "summary": "Mocked AI Response",
            "risk_level": "NOMINAL",
            "recommended_actions": [{"action": "test", "target_system": "test", "urgency": "LOW", "rank": 1}],
            "reasoning": "Mock reasoning",
            "confidence": 0.95
        })

# 1. Test Event Model Validation
def test_event_model_valid():
    evt = StadiumEvent(
        category=EventCategory.CROWD,
        severity=Severity.INFO,
        priority=Priority.LOW,
        source="Test-Src",
        location="Test-Loc",
        description="Test description",
        metrics={"test": True}
    )
    assert evt.category == EventCategory.CROWD
    assert evt.severity == Severity.INFO
    assert "Test-Src" in evt.source

# 2. Test Event Model Invalid
def test_event_model_invalid():
    with pytest.raises(ValueError):
        StadiumEvent(category="INVALID", severity="INVALID", priority="INVALID", source="", location="", description="", metrics={})

# 3. Test State Aggregator Update
def test_state_aggregator_update():
    agg = StadiumStateAggregator()
    evt = StadiumEvent(
        category=EventCategory.GATE,
        severity=Severity.CRITICAL,
        priority=Priority.HIGH,
        source="Gate 1",
        location="Gate 1",
        description="Gate Blocked",
        metrics={"flow": 0}
    )
    agg.update(evt)
    snapshot = agg.get_current_state()
    assert "GATE" in snapshot.subsystems
    assert "Gate 1" in snapshot.subsystems["GATE"]
    assert snapshot.subsystems["GATE"]["Gate 1"].health == "Critical"

# 4. Test State Aggregator Summary
def test_state_aggregator_summary():
    agg = StadiumStateAggregator()
    evt = StadiumEvent(
        category=EventCategory.GATE,
        severity=Severity.CRITICAL,
        priority=Priority.HIGH,
        source="Gate 1",
        location="Gate 1",
        description="Gate Blocked",
        metrics={"flow": 0}
    )
    agg.update(evt)
    summary = agg.get_operational_summary()
    assert "Critical" in summary
    assert "Gate 1" in summary

# 5. Test AI Manager execution
def test_ai_manager_execution():
    manager = AIManager(provider=MockAIProvider())
    manager.prompt_manager.get_prompt = MagicMock(return_value={"system": "", "developer": "", "user": ""})
    response = manager.execute_brain_task("copilot")
    assert isinstance(response, StadiumBrainResponse)
    assert response.summary == "Mocked AI Response"
    assert response.confidence == 0.95

# 6. Test AI Manager Fallback (Malformed JSON)
def test_ai_manager_malformed():
    class BadProvider(IAIProvider):
        def generate_response(self, system_prompt: str, user_prompt: str) -> str:
            return "{ bad json"
    
    manager = AIManager(provider=BadProvider())
    manager.prompt_manager.get_prompt = MagicMock(return_value={"system": "", "developer": "", "user": ""})
    
    # Should gracefully return a fallback response rather than crashing
    response = manager.execute_brain_task("copilot")
    assert response.risk_level == "WARNING"
    assert "SYSTEM FALLBACK" in response.summary
