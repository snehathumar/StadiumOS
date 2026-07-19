import json
from typing import List
from pydantic import BaseModel, Field
from backend.ai_brain.ai_manager import AIManager
from backend.ai_brain.agentic.models import AgentTask, ToolCall, AgentType
from backend.ai_brain.agentic.tools import TOOL_REGISTRY

class AgentToolResponse(BaseModel):
    """Schema for an agent's planned tool calls."""
    tool_calls: List[ToolCall]

class BaseSpecializedAgent:
    def __init__(self, agent_type: AgentType, allowed_tools: List[str]):
        self.agent_type = agent_type
        self.allowed_tools = allowed_tools
        self.ai = AIManager()

    def plan_tools(self, task: AgentTask) -> AgentTask:
        """Uses LLM to determine the exact tool calls needed for the task."""
        
        # Build prompt context manually for the agent
        system_prompt = (
            f"You are the Stadium {self.agent_type.value} Agent.\n"
            f"Your job is to solve the given task by selecting tools from your allowed registry.\n"
            f"ALLOWED TOOLS: {self.allowed_tools}\n"
            "You must return ONLY a JSON object matching the requested schema. No markdown wrapping."
        )
        
        user_prompt = f"Task Description: {task.description}\n\nGenerate the ToolCalls required."
        
        try:
            raw_output = self.ai._execute_with_retry(system_prompt, user_prompt)
            response = self.ai._parse_and_validate(raw_output, AgentToolResponse)
            
            # Filter tools to ensure they are allowed
            valid_calls = []
            for call in response.tool_calls:
                if call.tool_name in self.allowed_tools and call.tool_name in TOOL_REGISTRY:
                    valid_calls.append(call)
                    
            task.tool_calls = valid_calls
            
        except Exception as e:
            print(f"Agent {self.agent_type} failed to plan tools: {e}")
            task.tool_calls = []
            
        return task

# Initialize the concrete agents
crowd_agent = BaseSpecializedAgent(AgentType.CROWD, ["open_gate", "close_gate", "update_signage"])
security_agent = BaseSpecializedAgent(AgentType.SECURITY, ["allocate_security", "notify_staff"])
resource_agent = BaseSpecializedAgent(AgentType.RESOURCE, ["notify_staff", "log_operation"])
communication_agent = BaseSpecializedAgent(AgentType.COMMUNICATION, ["update_signage", "notify_staff", "log_operation"])

def get_agent_for_type(agent_type: AgentType) -> BaseSpecializedAgent:
    mapping = {
        AgentType.CROWD: crowd_agent,
        AgentType.SECURITY: security_agent,
        AgentType.RESOURCE: resource_agent,
        AgentType.COMMUNICATION: communication_agent,
        AgentType.PLANNER: resource_agent # Fallback
    }
    return mapping.get(agent_type, resource_agent)
