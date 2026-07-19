import json
from typing import Dict, Any
from backend.ai_brain.ai_manager import AIManager
from backend.ai_brain.context_builder import ContextBuilder
from backend.ai_brain.models import CopilotResponse
from backend.threat_engine.threat_engine import ThreatEngine
from backend.agents.evaluation.decision_logger import decision_logger

class StadiumCopilot:
    """
    Phase 5: Master AI Operations Assistant.
    Coordinates specialized virtual agents to provide conversational intelligence.
    """
    def __init__(self):
        self.ai = AIManager()
        self.context_builder = ContextBuilder()
        # In-memory history for multi-turn conversations
        self.memory_history = []
        
    def _route_intent(self, user_query: str) -> str:
        """Determines which specialized Agent Persona should handle the request."""
        q = user_query.lower()
        if any(w in q for w in ["what if", "if", "predict", "simulate", "happen if"]):
            return "Simulation Engine"
        elif any(w in q for w in ["crowd", "queue", "wait", "people", "congestion", "flow"]):
            return "Crowd Dynamics"
        elif any(w in q for w in ["threat", "security", "breach", "fight", "police", "incident"]):
            return "Security Intelligence"
        return "Master Operations"
        
    def ask(self, user_query: str) -> CopilotResponse:
        """
        Processes a natural language query and returns a structured operational response.
        """
        # 1. Intent Routing
        agent_type = self._route_intent(user_query)
        
        # 1b. Simulation Intercept
        if agent_type == "Simulation Engine":
            from backend.simulation.simulation_service import simulation_service
            sim_result = simulation_service.run_simulation(user_query)
            
            # Map SimulationResult to CopilotResponse for the chat interface
            action_items = []
            for i, opt in enumerate(sim_result.alternative_plans):
                from backend.ai_brain.models import CopilotAction
                action_items.append(CopilotAction(
                    priority=i+1,
                    action=opt.option_name,
                    location="Simulation Engine",
                    resource_required=opt.required_resources,
                    expected_result=f"Risk: {opt.risk_level} | Delay: {opt.expected_delay}"
                ))
                
            response = CopilotResponse(
                situation_summary=f"[SIMULATION: {sim_result.scenario}] {sim_result.current_state_summary}",
                risk_level=sim_result.risk.overall_risk,
                root_cause="Hypothetical Scenario",
                recommended_actions=action_items,
                expected_impact=sim_result.reasoning
            )
            self.memory_history.append({"user": user_query, "copilot_summary": response.situation_summary})
            return response
        
        # 2. Retrieve Live Context
        stadium_state = self.context_builder.build_context()
        
        # Build strict context payload
        custom_context = {
            "LIVE_STADIUM_STATE": stadium_state,
            "RECENT_CHAT_HISTORY": self.memory_history[-3:] # Context window
        }
        
        context_json = json.dumps(custom_context, indent=2)
        
        # 3. Delegate to AI Manager (Recommendation Agent)
        response: CopilotResponse = self.ai.execute_brain_task(
            template_name="copilot_chat",
            response_model=CopilotResponse,
            query=user_query,
            context=context_json,
            agent_type=agent_type
        )
        
        # 4. Update Memory
        self.memory_history.append({"user": user_query, "copilot_summary": response.situation_summary})
        
        # 5. Log Decision for Evaluation
        decision_logger.log(
            source=f"Copilot ({agent_type})", 
            input_context=user_query, 
            output_decision=f"Summary: {response.situation_summary} | Actions: {[a.action for a in response.recommended_actions]}"
        )
        
        return response
