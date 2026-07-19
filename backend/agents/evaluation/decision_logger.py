import datetime
from typing import List, Dict

class DecisionLogger:
    """Records operational recommendations made by Copilot and Agentic Ops."""
    def __init__(self):
        self.logs = []
        
    def log(self, source: str, input_context: str, output_decision: str):
        self.logs.append({
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "source": source,
            "input": input_context,
            "output": output_decision
        })
        
    def get_logs(self) -> List[Dict]:
        return list(reversed(self.logs))
        
decision_logger = DecisionLogger()
