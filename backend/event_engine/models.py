from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional

from config.constants import EventCategory, Severity, Priority, EventStatus

class StadiumEvent(BaseModel):
    """
    Unified JSON schema for all StadiumOS events.
    Enforces a strict contract across all modules.
    Maintains backward compatibility for Phase 1.
    """
    # Core Fields
    event_id: UUID = Field(default_factory=uuid4)
    schema_version: str = Field(default="v1.1", description="Schema versioning")
    category: EventCategory
    severity: Severity
    priority: Priority
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    source: str
    location: str
    metrics: Dict[str, Any]
    description: str
    
    # Status and Lifecycle
    status: EventStatus = Field(default=EventStatus.NEW)
    resolved: bool = Field(default=False)
    acknowledged: bool = Field(default=False)
    created_by: str = Field(default="system")
    last_updated: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    estimated_resolution_time: Optional[datetime] = None
    
    # Intelligence and Analysis
    confidence: float = Field(default=1.0, ge=0.0, le=1.0, description="AI/Sensor confidence score")
    tags: List[str] = Field(default_factory=list)
    recommended_action: Optional[str] = None
    
    # Correlation
    related_events: List[UUID] = Field(default_factory=list)
    root_cause: Optional[UUID] = None
    cascade_level: int = 0

    def to_json(self) -> str:
        """Returns the JSON string representation of the event."""
        # Using model_dump_json for Pydantic V2 compatibility
        if hasattr(self, 'model_dump_json'):
            return self.model_dump_json()
        return self.json()

    @classmethod
    def get_json_schema(cls) -> Dict[str, Any]:
        """Generate standard JSON schema for future API integration."""
        if hasattr(cls, 'model_json_schema'):
            return cls.model_json_schema()
        return cls.schema()
