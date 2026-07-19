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
    def __init__(self, model_name: str = None, api_key: str = None):
        import os
        from dotenv import load_dotenv
        load_dotenv()
        
        # Rule 2: ZERO Hardcoded Model Names
        self.model_name = model_name or os.getenv("DEFAULT_MODEL", "default")
        
        # Rule 1: Consistent API Key Variable
        resolved_key = api_key or os.getenv("GEMINI_API_KEY")
        if not resolved_key:
            try:
                import streamlit as st
                resolved_key = st.secrets.get("GEMINI_API_KEY")
            except Exception:
                pass
                
        self.api_key = resolved_key
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
                "recommended_actions": [{"action": "Continue standard operations", "target_system": "GLOBAL", "urgency": "LOW", "rank": 1}]
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
                    # Rule 3: Robust Auto-Fallback Mechanism
                    logger.error("All AI generation attempts failed. Engaging auto-fallback.")
                    raise RuntimeError("All API attempts failed")
                time.sleep(delay)
                delay *= 2  # Exponential backoff
                
    def _parse_and_validate(self, raw_json: str, response_model: Type[T]) -> T:
        """Strictly parses LLM JSON output into a Pydantic object."""
        try:
            cleaned = raw_json.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
                
            data = json.loads(cleaned)
            return response_model(**data)
        except Exception as e:
            logger.error(f"Failed to parse or validate JSON: {e}")
            raise ValueError(f"LLM returned invalid response: {e}")

    def execute_brain_task(self, template_name: str, response_model: Type[T] = StadiumBrainResponse, **kwargs) -> T:
        if "context" not in kwargs:
            context_dict = self.context_builder.build_context()
            kwargs["context"] = json.dumps(context_dict, indent=2)
        
        target_schema = response_model.model_json_schema()
        
        prompts = self.prompt_manager.get_prompt(
            template_name=template_name,
            schema=target_schema,
            **kwargs
        )
        
        anti_hallucination_rules = (
            "\nCRITICAL OPERATIONAL RULES:\n1. Strict adherence to schema."
        )
        combined_system = f"{prompts['system']}\n\n{prompts['developer']}\n{anti_hallucination_rules}"
        
        try:
            raw_output = self._execute_with_retry(combined_system, prompts["user"])
            return self._parse_and_validate(raw_output, response_model)
        except Exception as e:
            logger.error(f"Fallback triggered due to error: {e}")
            if response_model.__name__ == "CopilotResponse":
                return response_model(
                    situation_summary="SYSTEM FALLBACK: AI Service temporarily unavailable.",
                    risk_level="WARNING",
                    root_cause="API Offline",
                    recommended_actions=[],
                    expected_impact="Manual monitoring required"
                )
            elif response_model.__name__ == "SimulationResult":
                # Mocking nested models for simulation fallback
                return response_model(
                    scenario=kwargs.get("query", "Fallback"),
                    current_state_summary="API Unavailable",
                    predicted_state={"attendance": 0, "key_metrics": {}},
                    risk={"overall_risk": "WARNING", "crowd_risk": "WARNING", "security_risk": "WARNING", "operational_risk": "WARNING", "medical_risk": "WARNING"},
                    alternative_plans=[],
                    reasoning="API Offline"
                )
            else:
                return response_model(
                    summary="SYSTEM FALLBACK: AI Service temporarily unavailable.",
                    risk_level="WARNING",
                    recommended_actions=[],
                    reasoning="API Offline",
                    confidence=0.5
                )
