import os

class Settings:
    # Event Simulator Settings
    SIMULATOR_INTERVAL_SECONDS: float = float(os.getenv("SIMULATOR_INTERVAL_SECONDS", "1.0"))
    
    # Event Store Settings
    EVENT_HISTORY_BUFFER_SIZE: int = int(os.getenv("EVENT_HISTORY_BUFFER_SIZE", "500"))
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

settings = Settings()

# AI Settings
AI_CRITICAL_EVENT_LIMIT = 10
AI_WARNING_EVENT_LIMIT = 15
DEFAULT_CONFIDENCE_THRESHOLD = 0.85

# System Settings
ENABLE_AUTO_REFRESH = True
REFRESH_INTERVAL_SECONDS = 2
