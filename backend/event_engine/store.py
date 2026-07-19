import collections
from typing import List
from backend.event_engine.models import StadiumEvent
from config.constants import EventCategory
from config.settings import settings
from backend.event_engine.event_bus import event_bus, Subscriber
from utils.logger import logger

class EventStore(Subscriber):
    """
    In-memory history buffer for StadiumOS events.
    Automatically subscribes to the Event Bus to keep a rolling history.
    """
    def __init__(self, max_len: int = settings.EVENT_HISTORY_BUFFER_SIZE):
        self._buffer = collections.deque(maxlen=max_len)
        # Subscribe to all events (topic=None)
        event_bus.subscribe(self, topic=None)
        logger.info(f"Initialized EventStore with buffer size {max_len}")
        
    def update(self, event: StadiumEvent) -> None:
        """Callback to add events to the buffer."""
        self._buffer.append(event)
        
    def add_event(self, event: StadiumEvent) -> None:
        """Alias to add an event directly to the store."""
        self._buffer.append(event)
        
    def clear(self) -> None:
        """Clears all events from the history buffer."""
        self._buffer.clear()
        
    def get_recent_events(self, limit: int = 100) -> List[StadiumEvent]:
        """Returns the most recent N events."""
        events = list(self._buffer)
        return events[-limit:]
        
    def get_events_by_category(self, category: EventCategory, limit: int = 100) -> List[StadiumEvent]:
        """Returns recent events filtered by category."""
        events = [e for e in self._buffer if e.category == category]
        return events[-limit:]

# Global Event Store instance
event_store = EventStore()
