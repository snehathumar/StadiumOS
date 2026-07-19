import json
import time
import logging
from typing import Dict, Any, Type, TypeVar, Optional
from pydantic import BaseModel, ValidationError
from abc import ABC, abstractmethod

from backend.ai_brain.context_builder import ContextBuilder
from backend.ai_brain.prompt_manager import PromptManager
from backend.ai_brain.models import StadiumBrainResponse

logger = logging.getLogger("AIManager")
T = TypeVar('T', bound=BaseModel)

class IAIProvider(ABC):
    """Internal interface for the LLM provider."""
    @abstractmethod
    def generate_response(self, system_prompt: str, user_prompt: str) -> str:
        pass

class GeminiProvider(IAIProvider):
    """Concrete implementation for Google Gemini."""
    def __init__(self, model_name: str = "gemini-2.5-flash", api_key: str = None):
        self.model_name = model_name
        self.api_key = api_key
        self.is_configured = False
        
        try:
            import google.generativeai as genai
            if self.api_key:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel(self.model_name)
                self.is_configured = True
            else:
                logger.warning("Gemini API key missing. Operating in fallback simulation mode.")
        except ImportError:
            logger.warning("google-generativeai SDK not found. Operating in fallback simulation mode.")
            
    def generate_response(self, system_prompt: str, user_prompt: str) -> str:
        if not self.is_configured:
            # Simulation mode to prevent breaking the platform if API key isn't provided
            return json.dumps({
                "summary": "SIMULATED: All systems nominal.",
                "risk_level": "NOMINAL",
                "reasoning": "Simulation active. No real data analyzed.",
                "confidence": 0.99,
                "recommended_actions": [{"action": "Continue standard operations", "target_system": "GLOBAL", "urgency": "LOW"}]
            })
            
        try:
            # We construct a combined prompt for standard genai SDK
            full_prompt = f"SYSTEM INSTRUCTIONS:\n{system_prompt}\n\nUSER REQUEST:\n{user_prompt}"
            
            # Request strictly JSON format from Gemini 
            response = self.model.generate_content(
                full_prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            return response.text
        except Exception as e:
            logger.error(f"Gemini API failure: {str(e)}")
            raise

class AIManager:
    """
    Central orchestration for the StadiumOS AI Brain.
    Handles communication, retries, and strict structured parsing.
    """
    def __init__(self, provider: IAIProvider = None):
        self.provider = provider or GeminiProvider()
        self.prompt_manager = PromptManager()
        self.context_builder = ContextBuilder()
        
    def _execute_with_retry(self, system_prompt: str, user_prompt: str, max_retries: int = 3) -> str:
        """Handles network timeouts and API rate limits with exponential backoff."""
        delay = 2
        for attempt in range(max_retries):
            try:
                return self.provider.generate_response(system_prompt, user_prompt)
            except Exception as e:
                logger.warning(f"LLM request failed (attempt {attempt+1}/{max_retries}): {e}")
                if attempt == max_retries - 1:
                    raise
                time.sleep(delay)
                delay *= 2  # Exponential backoff
                
    def _parse_and_validate(self, raw_json: str, response_model: Type[T]) -> T:
        """Strictly parses LLM JSON output into a Pydantic object."""
        try:
            # Clean potential markdown wrapping if the LLM ignores instructions
            cleaned = raw_json.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
                
            data = json.loads(cleaned)
            return response_model(**data)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode LLM JSON: {e}\nRaw output: {raw_json}")
            raise ValueError("LLM returned malformed JSON.")
        except ValidationError as e:
            logger.error(f"LLM JSON failed schema validation: {e}")
            raise ValueError("LLM JSON did not match strict Pydantic schema.")

    def execute_brain_task(self, template_name: str, response_model: Type[T] = StadiumBrainResponse, **kwargs) -> T:
        """
        End-to-end generic flow enforcing strict anti-hallucination rules.
        Supports dynamic Pydantic schema injection.
        """
        # 1. Base Context (always retrieved to prevent inventing data)
        # We allow kwargs to override context if needed, but default to global state
        if "context" not in kwargs:
            context_dict = self.context_builder.build_context()
            kwargs["context"] = json.dumps(context_dict, indent=2)
        
        # 2. Template Extraction
        target_schema = response_model.model_json_schema()
        
        prompts = self.prompt_manager.get_prompt(
            template_name=template_name,
            schema=target_schema,
            **kwargs
        )
        
        # 3. Apply Global Security & Accuracy Rules
        anti_hallucination_rules = (
            "\nCRITICAL OPERATIONAL RULES:"
            "\n1. You are an experienced Stadium Operations Commander. Never answer casually."
            "\n2. Explain reasoning clearly step-by-step."
            "\n3. AVOID HALLUCINATIONS completely. NEVER invent sensor data."
            "\n4. If information is insufficient, explicitly state it in your reasoning and lower your confidence score."
            "\n5. If multiple actions exist, you MUST rank them sequentially starting at 1 based on urgency."
            "\n6. You must strictly adhere to the provided JSON schema."
            "\n7. YOU DO NOT DETECT THREATS. You only explain threats that have already been verified by the Rule Engine."
        )
        combined_system = f"{prompts['system']}\n\n{prompts['developer']}\n{anti_hallucination_rules}"
        
        # 4. Execute & Validate
        raw_output = self._execute_with_retry(combined_system, prompts["user"])
        return self._parse_and_validate(raw_output, response_model)
