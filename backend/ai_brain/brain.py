from typing import Optional
from backend.ai_brain.ai_manager import AIManager
from backend.ai_brain.models import StadiumBrainResponse

class StadiumBrain:
    """
    Central Intelligence Layer for StadiumOS.
    Acts as the primary facade for all backend AI operations.
    Strictly isolated from direct data stores and UI.
    """
    def __init__(self, ai_manager: Optional[AIManager] = None):
        self.ai = ai_manager or AIManager()
        
    def analyze_crowd(self) -> StadiumBrainResponse:
        """Evaluates crowd density and gate bottlenecks."""
        return self.ai.execute_brain_task("crowd_analysis")
        
    def recommend_actions(self) -> StadiumBrainResponse:
        """Generates global operational recommendations based on the current context."""
        return self.ai.execute_brain_task("operational_decision")
        
    def generate_sop(self, incident_details: str) -> StadiumBrainResponse:
        """Generates a standard operating procedure for a specific incident."""
        # We inject the specific incident as a 'message' while ContextBuilder provides the global state
        return self.ai.execute_brain_task("sop_generation", message=incident_details)
        
    def summarize_incidents(self) -> StadiumBrainResponse:
        """Provides an executive summary of recent critical warnings."""
        return self.ai.execute_brain_task("incident_summary")
        
    def explain_operational_risks(self) -> StadiumBrainResponse:
        """Analyzes active physical/cyber threats and evaluates risk."""
        return self.ai.execute_brain_task("threat_explanation")
        
    def support_weather_planning(self) -> StadiumBrainResponse:
        """Analyzes meteorological data and provides tactical recommendations."""
        return self.ai.execute_brain_task("weather_decision")
        
    def support_accessibility_guidance(self) -> StadiumBrainResponse:
        """Identifies mobility risks and recommends guest support actions."""
        return self.ai.execute_brain_task("accessibility_assistance")
        
    def support_navigation_advice(self, target_destination: str) -> StadiumBrainResponse:
        """Provides routing recommendations to bypass congestion."""
        # Requires adding a prompt to PromptManager dynamically or reusing operational_decision
        # Since we didn't define a specific navigation template in PromptManager earlier,
        # we can route this through 'operational_decision' with a specific message injection.
        return self.ai.execute_brain_task("operational_decision", message=f"Provide navigation route to: {target_destination}")
        
    def support_volunteer_guidance(self) -> StadiumBrainResponse:
        """Recommends deployment locations for volunteer staff."""
        return self.ai.execute_brain_task("operational_decision", message="Evaluate optimal volunteer deployment zones based on current crowd friction.")
