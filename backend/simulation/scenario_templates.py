from enum import Enum

class ScenarioType(str, Enum):
    CROWD_SURGE = "Crowd Surge"
    GATE_CLOSURE = "Gate Closure"
    HEAVY_RAIN = "Heavy Rain"
    VIP_ARRIVAL = "VIP Arrival"
    MEDICAL_EMERGENCY = "Medical Emergency"
    SECURITY_INCIDENT = "Security Incident"
    FIRE_ALARM = "Fire Alarm"
    PARTIAL_EVACUATION = "Partial Evacuation"
    FULL_EVACUATION = "Full Evacuation"
    NETWORK_FAILURE = "Network Failure"
    POWER_FAILURE = "Power Failure"
    PARKING_OVERFLOW = "Parking Overflow"
    CUSTOM = "Custom Scenario"
