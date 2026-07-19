from backend.agents.evaluation.confidence_engine import confidence_engine

class PerformanceAnalyzer:
    """Analyzes the hit/miss rate of predictions and decisions."""
    def __init__(self):
        self.total_decisions = 0
        self.successful_decisions = 0
        self.total_predictions = 0
        self.accurate_predictions = 0
        
    def log_decision_outcome(self, success: bool):
        self.total_decisions += 1
        if success:
            self.successful_decisions += 1
            confidence_engine.register_success()
        else:
            confidence_engine.register_failure()
            
    def log_prediction_outcome(self, accurate: bool):
        self.total_predictions += 1
        if accurate:
            self.accurate_predictions += 1
            confidence_engine.register_success()
        else:
            confidence_engine.register_failure()
            
    def get_metrics(self) -> dict:
        dec_acc = (self.successful_decisions / self.total_decisions * 100) if self.total_decisions > 0 else 100.0
        pred_acc = (self.accurate_predictions / self.total_predictions * 100) if self.total_predictions > 0 else 100.0
        
        return {
            "decision_accuracy": dec_acc,
            "prediction_accuracy": pred_acc,
            "total_evaluations": self.total_decisions + self.total_predictions,
            "current_confidence": confidence_engine.get_confidence()
        }

performance_analyzer = PerformanceAnalyzer()
