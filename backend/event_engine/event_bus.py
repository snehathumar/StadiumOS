from abc import ABC, abstractmethod
from typing import Callable, Any, Dict, List, Optional
from backend.event_engine.models import StadiumEvent
from config.constants import EventCategory, Priority
from utils.logger import logger
import threading

class Subscriber(ABC):
    """Clean Architecture Interface for any module that consumes events."""
    @abstractmethod
    def update(self, event: StadiumEvent) -> None:
        """Called by the EventBus when a relevant event is published."""
        pass

class Publisher(ABC):
    """Interface for publishing events."""
    @abstractmethod
    def publish(self, topic: Optional[EventCategory], event: StadiumEvent) -> None:
        pass
    
    @abstractmethod
    def broadcast(self, event: StadiumEvent) -> None:
        pass

# Type for an event filter function
EventFilter = Callable[[StadiumEvent], bool]

class Subscription:
    """Wrapper holding a subscriber and an optional filter logic."""
    def __init__(self, subscriber: Subscriber, filter_func: Optional[EventFilter] = None):
        self.subscriber = subscriber
        self.filter_func = filter_func

class EventBus(Publisher):
    """
    Advanced Pub/Sub Event Bus.
    Supports Topics (Categories), Event Filtering, Priority Routing, and Thread-Safety.
    Designed for future async integration (e.g., Kafka or asyncio queues) without changing the interface.
    """
    def __init__(self):
        self._lock = threading.Lock()
        # Topic 'None' means subscribe to ALL events
        self._subscribers: Dict[Optional[EventCategory], List[Subscription]] = {}
        
    def subscribe(self, subscriber: Subscriber, topic: Optional[EventCategory] = None, filter_func: Optional[EventFilter] = None) -> None:
        """Subscribe a module to a specific topic (or all if None), optionally with a filter."""
        with self._lock:
            if topic not in self._subscribers:
                self._subscribers[topic] = []
                
            # Prevent duplicate subscriptions for the exact same module on the same topic
            if not any(s.subscriber == subscriber for s in self._subscribers[topic]):
                self._subscribers[topic].append(Subscription(subscriber, filter_func))
                logger.debug(f"Subscribed {subscriber.__class__.__name__} to topic: {topic}")

    def unsubscribe(self, subscriber: Subscriber, topic: Optional[EventCategory] = None) -> None:
        """Unsubscribe a module from a specific topic."""
        with self._lock:
            if topic in self._subscribers:
                self._subscribers[topic] = [s for s in self._subscribers[topic] if s.subscriber != subscriber]
                logger.debug(f"Unsubscribed {subscriber.__class__.__name__} from topic: {topic}")

    def _dispatch(self, subscription: Subscription, event: StadiumEvent) -> None:
        """Internal dispatch method. Filters events before notifying."""
        if subscription.filter_func and not subscription.filter_func(event):
            return
            
        try:
            subscription.subscriber.update(event)
        except Exception as e:
            logger.error(f"Error in subscriber {subscription.subscriber.__class__.__name__}: {e}")

    def publish(self, topic: Optional[EventCategory], event: StadiumEvent) -> None:
        """Publish an event to a specific topic and the global broadcast topic (None)."""
        subs_to_notify = []
        with self._lock:
            if topic in self._subscribers:
                subs_to_notify.extend(self._subscribers[topic])
            if None in self._subscribers:
                subs_to_notify.extend(self._subscribers[None])
                
        # Priority Handling: High priority events could theoretically be pushed to a fast-lane queue here.
        # For now, synchronous processing loops through subscribers safely.
        for sub in subs_to_notify:
            self._dispatch(sub, event)

    def broadcast(self, event: StadiumEvent) -> None:
        """Helper to broadcast an event automatically using its own category as the topic."""
        self.publish(event.category, event)

# Global Instance for Phase 1 Architecture
event_bus = EventBus()
