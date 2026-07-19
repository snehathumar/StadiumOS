from enum import Enum

class Severity(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"

class Priority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

class EventStatus(str, Enum):
    NEW = "NEW"
    OPEN = "OPEN"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"

class EventCategory(str, Enum):
    CROWD = "CROWD"
    TICKET = "TICKET"
    WEATHER = "WEATHER"
    GATE = "GATE"
    MEDICAL = "MEDICAL"
    IOT = "IOT"
    NETWORK = "NETWORK"
