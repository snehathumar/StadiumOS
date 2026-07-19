import datetime
from typing import List, Dict

class Lesson:
    def __init__(self, context: str, failure_reason: str, corrective_action: str):
        self.timestamp = datetime.datetime.utcnow().isoformat()
        self.context = context
        self.failure_reason = failure_reason
        self.corrective_action = corrective_action

class LearningMemory:
    """Stores long-term operational lessons to inject into AI prompt context."""
    def __init__(self):
        self.lessons: List[Lesson] = []
        
    def add_lesson(self, context: str, failure_reason: str, corrective_action: str):
        self.lessons.append(Lesson(context, failure_reason, corrective_action))
        
    def get_recent_lessons(self) -> List[Dict]:
        return [{"context": l.context, "avoid": l.failure_reason, "do_instead": l.corrective_action} for l in self.lessons[-5:]]
        
learning_memory = LearningMemory()
