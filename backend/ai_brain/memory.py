import datetime
from typing import List, Dict
from backend.ai_brain.models import StadiumBrainResponse

class AIMemory:
    """
    Maintains a rolling buffer of recent AI operational decisions.
    Provides session context to prevent the AI from issuing contradictory
    recommendations in rapid succession.
    """
    def __init__(self, capacity: int = 10):
        self.capacity = capacity
        self.history: List[Dict[str, str]] = []
        
    def add_decision(self, task_type: str, response: StadiumBrainResponse) -> None:
        """Stores a summarized version of a decision."""
        record = {
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "task_type": task_type,
            "summary": response.summary,
            "actions_taken": [f"[{a.target_system}] {a.action}" for a in response.recommended_actions]
        }
        
        self.history.append(record)
        
        # Enforce capacity
        if len(self.history) > self.capacity:
            self.history.pop(0)
            
    def get_recent_decisions(self) -> List[Dict[str, str]]:
        """Returns the rolling memory buffer."""
        return self.history
    
    def clear(self) -> None:
        """Clears memory (useful for resetting drills or new match days)."""
        self.history.clear()
