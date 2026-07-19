from typing import List
from backend.ai_brain.agentic.models import AuditLogEntry

class AuditLogStore:
    """In-memory store for Agentic Operations audits."""
    def __init__(self):
        self.logs: List[AuditLogEntry] = []
        
    def add_entry(self, entry: AuditLogEntry):
        self.logs.append(entry)
        
    def get_logs(self) -> List[AuditLogEntry]:
        return list(reversed(self.logs))
        
audit_store = AuditLogStore()
