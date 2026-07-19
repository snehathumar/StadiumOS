from abc import ABC, abstractmethod
from typing import Optional, Tuple, List
from backend.event_engine.models import StadiumEvent
from backend.threat_engine.models import OperationalThreat

class IRuleEngine(ABC):
    """Interface for deterministic rule evaluation."""
    
    @abstractmethod
    def evaluate(self, event: StadiumEvent) -> Optional[OperationalThreat]:
        """Evaluates a raw event against all active rules and state buffers."""
        pass
        
    @abstractmethod
    def reload_rules(self) -> None:
        """Hot-reloads rules from configuration without rebooting."""
        pass
        
    @abstractmethod
    def enable_rule(self, rule_id: str) -> None:
        pass
        
    @abstractmethod
    def disable_rule(self, rule_id: str) -> None:
        pass

class IRiskCalculator(ABC):
    """Interface for deterministic risk scoring engines."""
    
    @abstractmethod
    def calculate(self, 
                  current_state: Any, 
                  active_threats: list, 
                  recent_events: list) -> 'RiskCalculationResult': # type: ignore
        """
        Calculates mathematical risk.
        Using Any for current_state to avoid circular imports with core.models.StadiumState
        """
        pass

class IIncidentManager(ABC):
    """Interface for managing the operational lifecycle of threats."""
    
    @abstractmethod
    def open_incident(self, threat: OperationalThreat) -> 'SecurityIncident': # type: ignore
        pass
        
    @abstractmethod
    def acknowledge(self, incident_id: str, owner: str) -> Optional['SecurityIncident']: # type: ignore
        pass
        
    @abstractmethod
    def resolve(self, incident_id: str, actor: str, resolution_notes: str) -> Optional['SecurityIncident']: # type: ignore
        pass
        
    @abstractmethod
    def escalate(self, incident_id: str, actor: str, reason: str) -> Optional['SecurityIncident']: # type: ignore
        pass
        
    @abstractmethod
    def reopen(self, incident_id: str, actor: str, reason: str) -> Optional['SecurityIncident']: # type: ignore
        pass
        
    @abstractmethod
    def get_incident(self, incident_id: str) -> Optional['SecurityIncident']: # type: ignore
        pass

class IActionRecommender(ABC):
    """Interface for generating and ranking operational responses to threats."""
    
    @abstractmethod
    def generate_recommendations(self, threat: OperationalThreat, risk_score: float) -> 'Tuple[List[RecommendedAction], Optional[ThreatExplanationResponse]]': # type: ignore
        """Returns prioritized actions AND the raw AI explanation context."""
        pass
