import json
from backend.ai_brain.ai_manager import AIManager
from backend.simulation.scenario_detector import scenario_detector
from backend.simulation.context_loader import context_loader
from backend.simulation.models import SimulationResult

class SimulationService:
    """Facade orchestrator for the predictive pipeline."""
    def __init__(self):
        self.ai = AIManager()

    def run_simulation(self, query: str) -> SimulationResult:
        """Executes a What-If simulation request."""
        
        # 1. Detect Scenario
        scenario = scenario_detector.detect(query)
        
        # 2. Load Current Context
        current_context = context_loader.load_context()
        
        # 3. Predict Future State, Estimate Risk, Recommend Actions
        # We use a single LLM execution here to reduce latency for the end user,
        # mapping the output directly into our granular Pipeline schemas.
        simulation_context = {
            "DETECTED_SCENARIO": scenario,
            "USER_QUERY": query,
            "LIVE_STADIUM_STATE": current_context
        }
        
        response: SimulationResult = self.ai.execute_brain_task(
            template_name="predictive_simulation",
            response_model=SimulationResult,
            query=query,
            context=json.dumps(simulation_context, indent=2)
        )
        
        # Override the scenario type if the detector found a known template
        # to ensure consistency, unless the LLM gave a better custom name for "Custom Scenario"
        if scenario != "Custom Scenario":
            response.scenario = scenario
            
        return response

simulation_service = SimulationService()
