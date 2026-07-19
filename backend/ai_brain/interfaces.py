from abc import ABC, abstractmethod
from typing import Dict, Any

class IContextBuilder(ABC):
    """
    Interface for safely retrieving and compressing stadium state into an LLM context.
    """
    @abstractmethod
    def build_context(self) -> Dict[str, Any]:
        pass

class IAIProvider(ABC):
    """
    Interface for the underlying Language Model provider.
    Ensures the Brain is decoupled from any specific API (e.g., Gemini, Claude).
    """
    @abstractmethod
    def generate_response(self, prompt: str, context: Dict[str, Any]) -> Any:
        pass
