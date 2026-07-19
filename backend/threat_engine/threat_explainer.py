import json
from typing import Dict, Any, Optional

from backend.threat_engine.models import OperationalThreat, ThreatExplanationResponse
from backend.ai_brain.ai_manager import AIManager
from backend.ai_brain.context_builder import ContextBuilder

class AIThreatExplainer:
    """
    Leverages the StadiumOS AI Brain to provide deterministic, human-readable
    explanations for threats.
    
    CRITICAL CONSTRAINT: The AI NEVER detects threats. It only explains threats 
    that have ALREADY been deterministically verified by the RuleEngine.
    """
    
    def __init__(self, ai_manager: Optional[AIManager] = None):
        self.ai = ai_manager or AIManager()
        self.context_builder = ContextBuilder()

    def explain_threat(self, threat: OperationalThreat, risk_score: float) -> ThreatExplanationResponse:
        """
        Takes a deterministically detected threat and queries the LLM for operational context,
        returning a strictly typed JSON schema response.
        """
        # 1. Gather all required context safely
        global_state = self.context_builder.build_context()
        
        # 2. Bind the exact threat data into the context so the AI doesn't hallucinate it
        custom_context = {
            "VERIFIED_THREAT": threat.model_dump(),
            "CALCULATED_RISK_SCORE": risk_score,
            "GLOBAL_STADIUM_STATE": global_state
        }
        
        context_json = json.dumps(custom_context, indent=2)
        
        # 3. Delegate to the AI Brain Orchestrator
        # We use the existing 'threat_explanation' template but override the response model
        response: ThreatExplanationResponse = self.ai.execute_brain_task(
            template_name="threat_explanation",
            response_model=ThreatExplanationResponse,
            context=context_json
        )
        
        return response
