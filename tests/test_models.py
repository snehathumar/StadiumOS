import pytest
from uuid import UUID
from datetime import datetime
from backend.event_engine.models import StadiumEvent, EventCategory, Severity, Priority, EventStatus

def test_stadium_event_creation():
    event = StadiumEvent(
        category=EventCategory.CROWD,
        severity=Severity.WARNING,
        priority=Priority.MEDIUM,
        source="TestSensor",
        location="Gate A",
        description="Test description",
        metrics={"test_metric": 123}
    )
    
    assert isinstance(event.event_id, UUID)
    assert event.category == EventCategory.CROWD
    assert event.severity == Severity.WARNING
    assert event.priority == Priority.MEDIUM
    assert event.source == "TestSensor"
    assert event.location == "Gate A"
    assert event.description == "Test description"
    assert event.metrics == {"test_metric": 123}
    assert event.status == EventStatus.NEW
    assert isinstance(event.timestamp, datetime)
    assert event.confidence == 1.0

def test_stadium_event_json_serialization():
    event = StadiumEvent(
        category=EventCategory.CROWD,
        severity=Severity.WARNING,
        priority=Priority.MEDIUM,
        source="TestSensor",
        location="Gate A",
        description="Test description",
        metrics={"test_metric": 123}
    )
    
    json_str = event.to_json()
    assert isinstance(json_str, str)
    assert "TestSensor" in json_str
    assert "Gate A" in json_str

def test_stadium_event_validation_error():
    with pytest.raises(ValueError):
        # Missing required fields
        StadiumEvent(
            source="TestSensor",
            location="Gate A",
            description="Test description",
            metrics={}
        )
