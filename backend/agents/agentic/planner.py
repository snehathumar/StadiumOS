import uuid
import datetime
from typing import List
from pydantic import BaseModel
from backend.ai_brain.ai_manager import AIManager
from backend.ai_brain.agentic.models import ExecutionPlan, AgentTask, AgentType
from backend.ai_brain.agentic.agents import get_agent_for_type

class PlannerResponse(BaseModel):
    """Schema for the Planner Agent's output."""
    tasks: List[AgentTask]

class PlannerAgent:
    """
    Translates a natural language operator goal into a structured Execution Plan
    and delegates the tasks to Specialized Agents to plan the ToolCalls.
    """
    def __init__(self):
        self.ai = AIManager()

    def create_plan(self, goal: str) -> ExecutionPlan:
        system_prompt = (
            "You are the StadiumOS Operations Planner Agent.\n"
            "Your job is to break down a high-level operational goal into sequential AgentTasks.\n"
            "Assign each task to the correct specialized agent type (CROWD, SECURITY, RESOURCE, COMMUNICATION).\n"
            "Do NOT define tool calls. The specialized agents will do that. Just define the tasks.\n"
            "Return valid JSON only matching the schema."
        )
        
        user_prompt = f"Operator Goal: {goal}\n\nGenerate the execution tasks."
        
        plan_id = f"PLAN-{uuid.uuid4().hex[:6].upper()}"
        
        try:
            raw_output = self.ai._execute_with_retry(system_prompt, user_prompt)
            response = self.ai._parse_and_validate(raw_output, PlannerResponse)
            
            # Ensure task IDs exist
            for idx, task in enumerate(response.tasks):
                if not task.task_id:
                    task.task_id = f"TSK-{idx+1}"
            
            plan = ExecutionPlan(
                plan_id=plan_id,
                goal=goal,
                tasks=response.tasks,
                created_at=datetime.datetime.utcnow().isoformat()
            )
            
            # Step 2: Delegate to Specialized Agents to populate tool calls
            self._delegate_to_agents(plan)
            
            return plan
            
        except Exception as e:
            print(f"Planner failed: {e}")
            return ExecutionPlan(
                plan_id=plan_id,
                goal=goal,
                tasks=[],
                status="FAILED",
                created_at=datetime.datetime.utcnow().isoformat()
            )
            
    def _delegate_to_agents(self, plan: ExecutionPlan):
        """Passes each task to its assigned specialized agent to plan tool calls."""
        for task in plan.tasks:
            agent = get_agent_for_type(task.assigned_agent)
            agent.plan_tools(task)
