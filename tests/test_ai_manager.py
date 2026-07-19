import pytest
import json
import sys
from unittest.mock import MagicMock
from backend.ai_brain.ai_manager import AIManager, GeminiProvider, IAIProvider
from backend.ai_brain.models import StadiumBrainResponse

# Mock generativeai to prevent ImportError/TypeError in tests
sys.modules['google.generativeai'] = MagicMock()

class MockFailedProvider(IAIProvider):
    def generate_response(self, system_prompt: str, user_prompt: str) -> str:
        raise Exception("API Timeout")

class MockSuccessProvider(IAIProvider):
    def generate_response(self, system_prompt: str, user_prompt: str) -> str:
        return json.dumps({
            "summary": "Test Summary",
            "risk_level": "NOMINAL",
            "recommended_actions": [],
            "reasoning": "Test Reasoning",
            "confidence": 1.0
        })

class MockMalformedProvider(IAIProvider):
    def generate_response(self, system_prompt: str, user_prompt: str) -> str:
        return "{ invalid_json "

def test_ai_manager_success():
    manager = AIManager(provider=MockSuccessProvider())
    # Use a real template name like "copilot" but we just want to bypass PromptManager error
    # Instead, let's mock prompt_manager
    manager.prompt_manager.get_prompt = MagicMock(return_value={"system": "sys", "developer": "dev", "user": "usr"})
    response = manager.execute_brain_task(template_name="copilot")
    
    assert isinstance(response, StadiumBrainResponse)
    assert response.summary == "Test Summary"
    assert response.risk_level == "NOMINAL"
    assert response.confidence == 1.0

def test_ai_manager_retry_failure():
    manager = AIManager(provider=MockFailedProvider())
    manager.prompt_manager.get_prompt = MagicMock(return_value={"system": "sys", "developer": "dev", "user": "usr"})
    with pytest.raises(Exception, match="API Timeout"):
        # We override _execute_with_retry to run faster for the test
        manager._execute_with_retry = lambda s, u, max_retries=1: manager.provider.generate_response(s, u)
        manager.execute_brain_task(template_name="test")

def test_ai_manager_malformed_json():
    manager = AIManager(provider=MockMalformedProvider())
    # Mock prompt_manager to avoid FileNotFoundError
    manager.prompt_manager.get_prompt = MagicMock(return_value={"system": "sys", "developer": "dev", "user": "usr"})
    with pytest.raises(ValueError, match="LLM returned malformed JSON."):
        manager.execute_brain_task(template_name="test")

def test_gemini_provider_fallback():
    # If no API key is provided, it should use fallback mode
    provider = GeminiProvider(api_key=None)
    # Ensure environment variable is not picked up for this test if it exists
    provider.is_configured = False
    
    response_str = provider.generate_response("sys", "usr")
    data = json.loads(response_str)
    
    assert data["risk_level"] == "NOMINAL"
    assert data["summary"] == "SIMULATED: All systems nominal."
