from typing import Callable, Dict, List, Optional
from backend.event_engine.models import StadiumEvent
from config.constants import EventCategory
from utils.logger import logger

# Type alias for subscribers
EventCallback = Callable[[StadiumEvent], None]

class EventBus:
    """
    A synchronous Pub/Sub Event Bus for StadiumOS.
    Allows modules (AI Brain, Copilot, Dashboards, State) to subscribe 
    to specific event categories without coupling to the generator.
    """
    def __init__(self):
        # Maps EventCategory to a list of callbacks
        self._subscribers: Dict[Optional[EventCategory], List[EventCallback]] = {}
    
    def subscribe(self, callback: EventCallback, category: Optional[EventCategory] = None) -> None:
        """
        Subscribe to events. 
        If category is None, subscribe to ALL events.
        """
        if category not in self._subscribers:
            self._subscribers[category] = []
        
        self._subscribers[category].append(callback)
        logger.debug(f"Subscribed callback {callback.__name__} to category {category}")

    def publish(self, event: StadiumEvent) -> None:
        """
        Publish an event to all relevant subscribers.
        """
        # Publish to category-specific subscribers
        if event.category in self._subscribers:
            for callback in self._subscribers[event.category]:
                try:
                    callback(event)
                except Exception as e:
                    logger.error(f"Error in subscriber {callback.__name__} for event {event.event_id}: {e}")
        
        # Publish to 'all events' subscribers (category=None)
        if None in self._subscribers:
            for callback in self._subscribers[None]:
                try:
                    callback(event)
                except Exception as e:
                    logger.error(f"Error in global subscriber {callback.__name__} for event {event.event_id}: {e}")

# Global Event Bus instance
event_bus = EventBus()
