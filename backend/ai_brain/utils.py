import json
from typing import Any

def count_approximate_tokens(text: str) -> int:
    """
    Utility to estimate token usage before sending to an LLM provider.
    Uses a fast word-count heuristic (average 0.75 words per token) 
    to avoid heavy dependencies like tiktoken in the core environment.
    """
    if not text:
        return 0
    words = len(text.split())
    return int(words / 0.75)

def pretty_print_json(data: Any) -> str:
    """
    Safely converts Pydantic objects or dictionaries to formatted JSON strings
    for UI display or debugging.
    """
    if hasattr(data, "model_dump"):
        data = data.model_dump()
    return json.dumps(data, indent=2)
