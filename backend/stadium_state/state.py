from typing import Dict, Any
from backend.event_engine.models import StadiumEvent
from config.constants import EventCategory
from backend.event_engine.bus import event_bus
from utils.logger import logger

class StadiumState:
    """
    Maintains the current 'snapshot' of the entire stadium.
    Instead of recalculating state from history, this object listens 
    to the Event Bus and continuously updates its internal fields.
    Future AI modules can query this for instant context.
    """
    def __init__(self):
        # We store the latest state grouped by category and location/source.
        self.state: Dict[str, Dict[str, Any]] = {
            category.value: {} for category in EventCategory
        }
        
        # Subscribe to all events
        event_bus.subscribe(self._on_event)
        logger.info("Initialized shared StadiumState")
        
    def _on_event(self, event: StadiumEvent) -> None:
        """
        Updates the global state based on incoming events.
        Different categories might key their state by location or source.
        """
        category_key = event.category.value
        
        # Use location as the primary key for state (e.g. 'Gate A')
        # If location is empty, fallback to source
        state_key = event.location if event.location else event.source
        
        # Store the latest metrics, severity and priority
        self.state[category_key][state_key] = {
            "metrics": event.metrics,
            "severity": event.severity.value,
            "priority": event.priority.value,
            "last_updated": event.timestamp.isoformat(),
            "description": event.description
        }
        
    def get_snapshot(self) -> Dict[str, Any]:
        """Returns a copy of the complete current stadium state."""
        return self.state
        
    def get_category_state(self, category: EventCategory) -> Dict[str, Any]:
        """Returns the current state for a specific category."""
        return self.state.get(category.value, {})

# Global Stadium State instance
stadium_state = StadiumState()
