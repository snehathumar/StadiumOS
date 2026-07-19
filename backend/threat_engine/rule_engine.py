import json
import os
import uuid
import datetime
from typing import List, Dict, Optional, Any

from backend.event_engine.models import StadiumEvent
from backend.threat_engine.models import SecurityRule, OperationalThreat, RuleCondition
from backend.threat_engine.interfaces import IRuleEngine

class RuleEngine(IRuleEngine):
    """
    Deterministic rule evaluation engine for Threat Intelligence.
    Converts raw events into actionable Operational Threats based on JSON configurations.
    """
    def __init__(self, rules_file: str = "security/rules.json"):
        self.rules_file = rules_file
        self.rules: List[SecurityRule] = []
        
        # State tracking for time-based thresholds
        # Format: rule_id -> { location -> [Event] }
        self.state_buffer: Dict[str, Dict[str, List[StadiumEvent]]] = {}
        
        self.reload_rules()

    def reload_rules(self) -> None:
        """Loads or hot-reloads the rule configurations."""
        self.rules.clear()
        self.state_buffer.clear()
        
        if not os.path.exists(self.rules_file):
            return
            
        with open(self.rules_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for r in data:
                rule = SecurityRule(**r)
                self.rules.append(rule)
                self.state_buffer[rule.rule_id] = {}

    def enable_rule(self, rule_id: str) -> None:
        for r in self.rules:
            if r.rule_id == rule_id:
                r.enabled = True

    def disable_rule(self, rule_id: str) -> None:
        for r in self.rules:
            if r.rule_id == rule_id:
                r.enabled = False

    def _resolve_field(self, event: StadiumEvent, field_path: str) -> Any:
        """Dynamically resolves nested properties via string paths (e.g. 'category.value')."""
        parts = field_path.split('.')
        val = event
        try:
            for part in parts:
                val = getattr(val, part)
            return val
        except AttributeError:
            return None

    def _evaluate_condition(self, condition: RuleCondition, event: StadiumEvent) -> bool:
        """Evaluates a single deterministic logic condition."""
        actual_val = self._resolve_field(event, condition.field)
        
        if actual_val is None:
            return False
            
        if condition.operator == "==":
            return actual_val == condition.value
        elif condition.operator == ">":
            return actual_val > condition.value
        elif condition.operator == "<":
            return actual_val < condition.value
        elif condition.operator == "contains":
            return str(condition.value).lower() in str(actual_val).lower()
        elif condition.operator == "in":
            return actual_val in condition.value
            
        return False

    def evaluate(self, event: StadiumEvent) -> Optional[OperationalThreat]:
        """
        Runs an event through all enabled rules.
        Returns an OperationalThreat if thresholds are breached.
        """
        now = datetime.datetime.utcnow()
        
        for rule in self.rules:
            if not rule.enabled:
                continue
                
            # 1. Check all conditions
            matches = True
            for cond in rule.conditions:
                if not self._evaluate_condition(cond, event):
                    matches = False
                    break
                    
            # 2. Handle matched events
            if matches:
                loc = event.location
                if loc not in self.state_buffer[rule.rule_id]:
                    self.state_buffer[rule.rule_id][loc] = []
                    
                buffer = self.state_buffer[rule.rule_id][loc]
                buffer.append(event)
                
                # 3. Prune old events outside the time window
                if rule.threshold_window_sec > 0:
                    buffer = [e for e in buffer if (now - e.timestamp).total_seconds() <= rule.threshold_window_sec]
                    self.state_buffer[rule.rule_id][loc] = buffer
                    
                # 4. Trigger Threat if threshold met
                if len(buffer) >= rule.threshold_count:
                    threat = OperationalThreat(
                        threat_id=str(uuid.uuid4()),
                        rule_id=rule.rule_id,
                        name=rule.generated_threat_name,
                        category=rule.category,
                        severity=rule.severity,
                        priority=rule.priority,
                        location=event.location,
                        timestamp=now.isoformat(),
                        description=f"Automated threat detection triggered by {len(buffer)} matching events.",
                        recommended_action=rule.recommended_action,
                        status="DETECTED",
                        triggering_events=[str(e.event_id) for e in buffer]
                    )
                    
                    # Clear buffer to prevent immediate duplicate threat firing
                    self.state_buffer[rule.rule_id][loc] = []
                    
                    return threat
                    
        return None
