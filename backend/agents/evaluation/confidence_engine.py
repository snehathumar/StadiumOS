class ConfidenceEngine:
    """Dynamically adjusts the AI's internal confidence based on performance history."""
    def __init__(self):
        self.base_confidence = 0.95
        
    def register_success(self):
        self.base_confidence = min(1.0, self.base_confidence + 0.02)
        
    def register_failure(self):
        self.base_confidence = max(0.1, self.base_confidence - 0.15)
        
    def get_confidence(self) -> float:
        return self.base_confidence

confidence_engine = ConfidenceEngine()
