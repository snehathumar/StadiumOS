from typing import List, Dict, Any, Tuple
from backend.threat_engine.models import RiskCalculationResult, SubsystemRisk, OperationalThreat
from backend.threat_engine.interfaces import IRiskCalculator
from backend.event_engine.models import StadiumEvent

class RiskCalculator(IRiskCalculator):
    """
    Deterministic mathematical engine for computing Stadium Risk.
    Uses configurable weights, active threats, and event velocity to generate 
    a highly explainable, transparent 0-100 risk score.
    """
    
    def __init__(self, config: Dict[str, float] = None):
        # Configurable base weights for Subsystems
        self.weights = config or {
            "CROWD": 1.5,
            "WEATHER": 1.2,
            "SECURITY": 2.0,
            "MEDICAL": 1.8,
            "GATE": 1.0,
            "NETWORK": 0.8,
            "IOT": 0.5,
            "TICKET": 0.8
        }
        
        # Threat Severity Multipliers
        self.severity_multipliers = {
            "LOW": 5.0,
            "MEDIUM": 15.0,
            "HIGH": 40.0,
            "CRITICAL": 80.0
        }
        
        # State tracking for trend
        self.previous_score = 0.0

    def _determine_category(self, score: float) -> str:
        if score < 20: return "NOMINAL"
        if score < 50: return "ELEVATED"
        if score < 80: return "HIGH"
        return "CRITICAL"

    def calculate(self, current_state: Any, active_threats: List[OperationalThreat], recent_events: List[StadiumEvent]) -> RiskCalculationResult:
        explain_log = ["--- Risk Calculation Start ---"]
        subsystem_scores: Dict[str, float] = {k: 0.0 for k in self.weights.keys()}
        subsystem_factors: Dict[str, List[str]] = {k: [] for k in self.weights.keys()}
        
        confidence = 1.0
        
        # 1. Process Active Threats (Heaviest Weight)
        if active_threats:
            explain_log.append(f"Evaluating {len(active_threats)} active threats.")
            for threat in active_threats:
                cat = threat.category.upper()
                if cat not in self.weights:
                    cat = "SECURITY" # Default mapping
                    
                penalty = self.severity_multipliers.get(threat.severity.value, 10.0)
                weighted_penalty = penalty * self.weights.get(cat, 1.0)
                
                subsystem_scores[cat] += weighted_penalty
                subsystem_factors[cat].append(f"Active Threat: {threat.name} ({threat.severity.value}) -> +{weighted_penalty:.1f} pts")
                explain_log.append(f"Applied {weighted_penalty:.1f} penalty to {cat} due to {threat.name}.")
        else:
            explain_log.append("No active threats detected. Threat modifier is 0.")

        # 2. Process Recent Events (Velocity / Noise Weight)
        if recent_events:
            explain_log.append(f"Evaluating {len(recent_events)} recent events for velocity penalties.")
            warning_count = 0
            critical_count = 0
            
            for event in recent_events:
                if event.severity.value == "WARNING":
                    warning_count += 1
                elif event.severity.value == "CRITICAL":
                    critical_count += 1
                    
            if warning_count > 0:
                global_penalty = warning_count * 1.5
                explain_log.append(f"Applied general velocity penalty (+{global_penalty}) for {warning_count} warnings.")
                subsystem_scores["CROWD"] += global_penalty / 2 # Distribute arbitrarily for simulation
            if critical_count > 0:
                global_penalty = critical_count * 3.0
                explain_log.append(f"Applied severe velocity penalty (+{global_penalty}) for {critical_count} critical events.")
                subsystem_scores["SECURITY"] += global_penalty / 2
        
        # 3. Assess State Completeness (Confidence)
        if not current_state:
            explain_log.append("WARNING: No current state provided. Confidence downgraded.")
            confidence = 0.5
        else:
            explain_log.append("Current state snapshot present. Confidence is High.")
            
        # 4. Compile Subsystems and Global Score
        total_risk = 0.0
        max_possible_weight = sum(self.weights.values()) * 100
        compiled_subsystems = []
        
        for category, raw_score in subsystem_scores.items():
            # Cap subsystem score at 100
            capped_score = min(raw_score, 100.0)
            if capped_score > 0:
                compiled_subsystems.append(
                    SubsystemRisk(
                        category=category,
                        score=capped_score,
                        factors=subsystem_factors.get(category, [])
                    )
                )
            
            # Global formula: (Subsystem Score * Subsystem Weight)
            total_risk += capped_score * self.weights.get(category, 1.0)
            
        # Normalize global score to 0-100
        final_score = (total_risk / max_possible_weight) * 100 if max_possible_weight > 0 else 0.0
        final_score = min(final_score, 100.0)
        
        # 5. Trend Calculation
        trend = "STABLE"
        if final_score > self.previous_score + 5:
            trend = "RISING"
        elif final_score < self.previous_score - 5:
            trend = "FALLING"
            
        self.previous_score = final_score
        
        explain_log.append(f"Final Global Score: {final_score:.1f}/100.0")
        explain_log.append(f"Calculated Trend: {trend}")
        
        return RiskCalculationResult(
            overall_score=final_score,
            risk_category=self._determine_category(final_score),
            trend=trend,
            confidence_score=confidence,
            subsystem_risks=compiled_subsystems,
            explainability_log=explain_log
        )
