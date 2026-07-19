import uuid
import datetime
import threading
from typing import Dict, Optional, List

from backend.threat_engine.models import (
    OperationalThreat, 
    SecurityIncident, 
    IncidentStatus, 
    IncidentTimelineEvent
)
from backend.threat_engine.interfaces import IIncidentManager

class IncidentManager(IIncidentManager):
    """
    Thread-safe operational lifecycle manager for security threats.
    Upgrades raw threats into tracked incidents with owners and timelines.
    """
    
    def __init__(self):
        # In-memory storage mapping incident_id -> SecurityIncident
        self._incidents: Dict[str, SecurityIncident] = {}
        # Protects access to the incident dictionary
        self._lock = threading.Lock()

    def _now(self) -> str:
        return datetime.datetime.utcnow().isoformat()

    def _add_timeline_event(self, incident: SecurityIncident, action: str, actor: str, notes: Optional[str] = None):
        """Helper to append to an incident's immutable timeline."""
        incident.timeline.append(
            IncidentTimelineEvent(
                timestamp=self._now(),
                action=action,
                actor=actor,
                notes=notes
            )
        )
        incident.updated_at = self._now()

    def open_incident(self, threat: OperationalThreat) -> SecurityIncident:
        """Converts a raw threat into a trackable operational incident."""
        incident_id = f"INC-{str(uuid.uuid4())[:8].upper()}"
        now_str = self._now()
        
        timeline_init = IncidentTimelineEvent(
            timestamp=now_str,
            action="OPENED",
            actor="SYSTEM",
            notes=f"Automated creation from Threat: {threat.name}"
        )
        
        incident = SecurityIncident(
            incident_id=incident_id,
            threat_id=threat.threat_id,
            title=f"Investigate: {threat.name}",
            status=IncidentStatus.OPEN,
            severity=threat.severity,
            priority=threat.priority,
            created_at=now_str,
            updated_at=now_str,
            timeline=[timeline_init]
        )
        
        with self._lock:
            self._incidents[incident_id] = incident
            
        return incident

    def acknowledge(self, incident_id: str, owner: str) -> Optional[SecurityIncident]:
        """Marks an incident as acknowledged by a specific human/AI operator."""
        with self._lock:
            incident = self._incidents.get(incident_id)
            if not incident:
                return None
                
            if incident.status in [IncidentStatus.RESOLVED]:
                # Cannot acknowledge a resolved incident
                return incident
                
            incident.status = IncidentStatus.ACKNOWLEDGED
            incident.owner = owner
            self._add_timeline_event(incident, "ACKNOWLEDGED", owner, "Operator took ownership of the incident.")
            return incident

    def resolve(self, incident_id: str, actor: str, resolution_notes: str) -> Optional[SecurityIncident]:
        """Closes an incident and attaches the post-mortem/resolution notes."""
        with self._lock:
            incident = self._incidents.get(incident_id)
            if not incident:
                return None
                
            incident.status = IncidentStatus.RESOLVED
            self._add_timeline_event(incident, "RESOLVED", actor, resolution_notes)
            return incident

    def escalate(self, incident_id: str, actor: str, reason: str) -> Optional[SecurityIncident]:
        """Increases priority and alters status when standard procedures fail."""
        with self._lock:
            incident = self._incidents.get(incident_id)
            if not incident:
                return None
                
            incident.status = IncidentStatus.ESCALATED
            incident.priority = max(1, incident.priority - 1)  # 1 is highest priority
            self._add_timeline_event(incident, "ESCALATED", actor, reason)
            return incident

    def reopen(self, incident_id: str, actor: str, reason: str) -> Optional[SecurityIncident]:
        """Allows closed incidents to be reopened if the threat re-emerges."""
        with self._lock:
            incident = self._incidents.get(incident_id)
            if not incident:
                return None
                
            if incident.status != IncidentStatus.RESOLVED:
                return incident # Only resolved incidents can be reopened
                
            incident.status = IncidentStatus.OPEN
            incident.owner = None # Strip owner to force re-acknowledgement
            self._add_timeline_event(incident, "REOPENED", actor, reason)
            return incident

    def get_incident(self, incident_id: str) -> Optional[SecurityIncident]:
        """Safe retrieval of current state."""
        with self._lock:
            # We return the object itself; in a real distributed system we might deepcopy to prevent outside mutation,
            # but for this architecture, we rely on Pydantic's internal state.
            return self._incidents.get(incident_id)
            
    def get_all_active_incidents(self) -> List[SecurityIncident]:
        """Utility for dashboards to fetch ongoing work."""
        with self._lock:
            return [
                inc for inc in self._incidents.values() 
                if inc.status != IncidentStatus.RESOLVED
            ]
