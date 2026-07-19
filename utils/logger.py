import logging
import sys
from config.settings import settings

def setup_logger(name: str) -> logging.Logger:
    """Sets up and returns a standard logger."""
    logger = logging.getLogger(name)
    
    # Avoid adding handlers multiple times if instantiated multiple times
    if not logger.handlers:
        logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO))
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Console handler
        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        
        # We can add file handlers later if needed.
        
    return logger

# Global default logger
logger = setup_logger("stadiumos")
