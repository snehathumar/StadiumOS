from backend.simulation.scenario_templates import ScenarioType

class ScenarioDetector:
    """Parses natural language simulation requests into known templates."""
    def detect(self, query: str) -> str:
        q = query.lower()
        if any(w in q for w in ["rain", "storm", "weather", "lightning"]):
            return ScenarioType.HEAVY_RAIN.value
        elif any(w in q for w in ["close gate", "gate closes", "gate down"]):
            return ScenarioType.GATE_CLOSURE.value
        elif any(w in q for w in ["surge", "more fans", "arrive", "crowd", "rush"]):
            return ScenarioType.CROWD_SURGE.value
        elif any(w in q for w in ["fight", "security", "breach", "intruder"]):
            return ScenarioType.SECURITY_INCIDENT.value
        elif any(w in q for w in ["medical", "sick", "injury"]):
            return ScenarioType.MEDICAL_EMERGENCY.value
        elif any(w in q for w in ["evacuate", "evacuation", "fire"]):
            return ScenarioType.FULL_EVACUATION.value
        elif any(w in q for w in ["power", "outage", "blackout"]):
            return ScenarioType.POWER_FAILURE.value
        return ScenarioType.CUSTOM.value

scenario_detector = ScenarioDetector()
