from pydantic import BaseModel, Field
from typing import List, Dict, Any

class PredictedState(BaseModel):
    attendance: str = Field(description="Predicted total attendance as a string (e.g. '80,000')")
    key_metrics: Dict[str, str] = Field(description="Key metrics (e.g. {'Gate A Density': '95%', 'Queue Time': '22 minutes'})")

class RiskProfile(BaseModel):
    overall_risk: str = Field(description="LOW, MEDIUM, HIGH, or CRITICAL")
    crowd_risk: str = Field(description="LOW, MEDIUM, HIGH, or CRITICAL")
    security_risk: str = Field(description="LOW, MEDIUM, HIGH, or CRITICAL")
    operational_risk: str = Field(description="LOW, MEDIUM, HIGH, or CRITICAL")
    medical_risk: str = Field(description="LOW, MEDIUM, HIGH, or CRITICAL")

class StrategicOption(BaseModel):
    option_name: str = Field(description="e.g. 'OPTION A: Do Nothing', 'OPTION B: Open Gate C'")
    actions: List[str] = Field(description="Specific actions to take")
    risk_level: str = Field(description="Expected risk if this option is taken (LOW, MEDIUM, HIGH, CRITICAL)")
    expected_delay: str = Field(description="e.g. '25 min'")
    required_resources: str = Field(description="e.g. 'None', '10 Security Guards'")

class RecommendationItem(BaseModel):
    priority: int = Field(description="1 is highest priority")
    action: str = Field(description="e.g. 'Open Gate C', 'Deploy additional security'")
    expected_benefit: str = Field(description="Why we should do this")
    estimated_impact: str = Field(description="e.g. 'Reduces queue by 10 mins'")
    required_resources: str = Field(description="Resources needed")

class SimulationResult(BaseModel):
    scenario: str = Field(description="The detected ScenarioType or custom scenario name")
    current_state_summary: str = Field(description="Brief summary of the current state before simulation")
    predicted_state: PredictedState
    risk: RiskProfile
    recommendations: List[RecommendationItem]
    alternative_plans: List[StrategicOption]
    reasoning: str = Field(description="Detailed explanation of WHY this prediction was made based on the data")
