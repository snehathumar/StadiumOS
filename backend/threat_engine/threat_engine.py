from typing import Optional, Any, List
from backend.event_engine.models import StadiumEvent
from backend.threat_engine.models import EnrichedOperationalThreat
from backend.threat_engine.interfaces import IRuleEngine, IRiskCalculator, IIncidentManager, IActionRecommender
from backend.threat_engine.rule_engine import RuleEngine
from backend.threat_engine.risk_calculator import RiskCalculator
from backend.threat_engine.incident_manager import IncidentManager
from backend.threat_engine.action_recommender import ActionRecommender

class ThreatEngine:
    """
    Master Orchestrator for Phase 4A: Threat Intelligence.
    Strictly coordinates decoupled dependencies to ensure deterministic detection
    is NEVER reliant on AI, while still returning a unified Enriched response.
    """
    def __init__(self,
                 rule_engine: Optional[IRuleEngine] = None,
                 risk_calculator: Optional[IRiskCalculator] = None,
                 incident_manager: Optional[IIncidentManager] = None,
                 action_recommender: Optional[IActionRecommender] = None):
                 
        self.rules = rule_engine or RuleEngine()
        self.risk = risk_calculator or RiskCalculator()
        self.incidents = incident_manager or IncidentManager()
        self.recommender = action_recommender or ActionRecommender()

    def process_event(self, event: StadiumEvent, current_state: Any = None, recent_events: List[StadiumEvent] = None) -> Optional[EnrichedOperationalThreat]:
        """
        Ingests a raw event and orchestrates the full security pipeline.
        Returns a master payload containing all detection, risk, lifecycle, and AI intelligence.
        """
        # 1. Deterministic Detection (NO AI)
        threat = self.rules.evaluate(event)
        if not threat:
            return None
            
        recent_events = recent_events or []
            
        # 2. Mathematical Risk Calculation (NO AI)
        risk_result = self.risk.calculate(current_state, [threat], recent_events)
        
        # 3. Incident Lifecycle Tracking (NO AI)
        incident = self.incidents.open_incident(threat)
        
        # 4. Action Recommendation & AI Explanation (AI ONLY used here)
        actions, explanation = self.recommender.generate_recommendations(threat, risk_result.overall_score)
        
        # Fallback values if AI provider is offline or rate-limited
        reasoning = "Deterministic rule triggered. AI explanation unavailable."
        mitigation_plan = ["Follow standard operating procedures."]
        confidence = 1.0
        
        if explanation:
            reasoning = explanation.reasoning
            mitigation_plan = explanation.mitigation_steps
            confidence = explanation.confidence
            
        # 5. Assemble Unified Master Payload
        enriched_threat = EnrichedOperationalThreat(
            threat_id=threat.threat_id,
            incident_id=incident.incident_id,
            rule_name=threat.name,
            risk_score=risk_result.overall_score,
            severity=threat.severity,
            priority=threat.priority,
            confidence=confidence,
            recommended_actions=actions,
            current_status=incident.status,
            reasoning=reasoning,
            mitigation_plan=mitigation_plan,
            timeline=incident.timeline
        )
        
        return enriched_threat
