from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from enum import Enum

class AgentType(str, Enum):
    CROWD = "CROWD"
    SECURITY = "SECURITY"
    RESOURCE = "RESOURCE"
    COMMUNICATION = "COMMUNICATION"
    PLANNER = "PLANNER"

class ToolCall(BaseModel):
    tool_name: str
    arguments: Dict[str, Any]
    reasoning: str

class AgentTask(BaseModel):
    task_id: str
    description: str
    assigned_agent: AgentType
    required_tools: List[str]
    tool_calls: List[ToolCall] = Field(default_factory=list, description="Specific actions planned by the assigned agent")
    status: str = "PENDING" # PENDING, IN_PROGRESS, COMPLETED, FAILED
    result_message: Optional[str] = None

class ExecutionPlan(BaseModel):
    plan_id: str
    goal: str
    tasks: List[AgentTask]
    status: str = "AWAITING_APPROVAL" # AWAITING_APPROVAL, APPROVED, EXECUTING, SUCCESS, FAILED
    created_at: str

class AuditLogEntry(BaseModel):
    timestamp: str
    operator_request: str
    plan_id: str
    tools_used: List[str]
    execution_status: str
