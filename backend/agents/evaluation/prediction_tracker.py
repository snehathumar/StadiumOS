class PredictionTracker:
    """Tracks Phase 6 Simulations to later evaluate their accuracy against reality."""
    def __init__(self):
        self.predictions = []
        
    def track(self, scenario: str, predicted_state: dict):
        self.predictions.append({
            "scenario": scenario,
            "predicted_state": predicted_state,
            "status": "PENDING_VERIFICATION"
        })
        
    def get_pending(self) -> list:
        return [p for p in self.predictions if p["status"] == "PENDING_VERIFICATION"]

prediction_tracker = PredictionTracker()
