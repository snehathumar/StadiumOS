from pydantic import BaseModel, Field
from typing import List, Dict, Any

class SystemSummary(BaseModel):
    """Summarizes a specific subsystem (e.g. CROWD, WEATHER) at a given point in time."""
    health: str = Field(description="Health level: GOOD, WARNING, or CRITICAL")
    status: str = Field(description="Brief text summary of the operational status")
    last_updated: str = Field(description="ISO timestamp of last update")
    metrics: Dict[str, Any] = Field(default_factory=dict, description="Aggregated telemetry")

class IncidentSummary(BaseModel):
    """Compressed representation of one or more similar events."""
    category: str
    severity: str
    location: str
    description: str
    count: int = Field(default=1, description="Number of times this similar event occurred recently")

class OperationalContext(BaseModel):
    """
    The master context object provided to the AI.
    Contains no raw event history, only structured, aggregated, and compressed intelligence.
    """
    timestamp: str
    global_health: str
    crowd: SystemSummary
    weather: SystemSummary
    medical: SystemSummary
    gate: SystemSummary
    network: SystemSummary
    iot: SystemSummary
    threat: SystemSummary
    critical_incidents: List[IncidentSummary]
    recent_warnings: List[IncidentSummary]

class ActionItem(BaseModel):
    """A structured recommendation from the AI."""
    rank: int = Field(description="Priority rank of the action (1 is highest priority)")
    action: str = Field(description="The concrete action to take")
    target_system: str = Field(description="The subsystem to target (e.g. CROWD, GATE, SECURITY)")
    urgency: str = Field(description="HIGH, MEDIUM, or LOW")

class StadiumBrainResponse(BaseModel):
    """
    Unified, strict JSON response schema enforced across all Brain capabilities.
    """
    summary: str = Field(description="Executive summary of the situation")
    risk_level: str = Field(description="CRITICAL, WARNING, or NOMINAL")
    recommended_actions: List[ActionItem] = Field(description="List of actionable recommendations")
    reasoning: str = Field(description="Detailed explanation of why these actions were chosen based purely on context data")
    confidence: float = Field(description="Confidence score from 0.0 to 1.0. If data is insufficient, lower this score.")

class CopilotAction(BaseModel):
    """Structured action for the Copilot."""
    priority: int = Field(description="1 is highest priority")
    action: str = Field(description="The concrete action to take")
    location: str = Field(description="Target location for the action (e.g., 'Gate A', 'Stadium-Wide')")
    resource_required: str = Field(description="Resources needed (e.g. '5 Security Staff')")
    expected_result: str = Field(description="What this action will achieve")

class CopilotResponse(BaseModel):
    """Unified response schema for the StadiumOS Copilot."""
    situation_summary: str = Field(description="Clear summary of current context answering the user's query")
    risk_level: str = Field(description="CRITICAL, HIGH, MEDIUM, LOW, or NOMINAL")
    root_cause: str = Field(description="Identified cause of any active issue, or 'N/A'")
    recommended_actions: List[CopilotAction] = Field(description="Ranked list of actions")
    expected_impact: str = Field(description="Overall operational impact if actions are taken")
