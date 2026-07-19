import json
from typing import Dict, Any, Optional

class PromptTemplate:
    """
    Represents a versioned, multi-lingual prompt template.
    Strictly separates the System, Developer, and User roles.
    """
    def __init__(self, name: str, version: str = "1.0"):
        self.name = name
        self.version = version
        self.system_prompt: Dict[str, str] = {}
        self.developer_prompt: Dict[str, str] = {}
        self.user_prompt_template: Dict[str, str] = {}
        
    def add_language(self, lang: str, system: str, developer: str, user: str) -> None:
        """Adds template strings for a specific language."""
        self.system_prompt[lang] = system
        self.developer_prompt[lang] = developer
        self.user_prompt_template[lang] = user

    def render(self, lang: str = "en", **kwargs) -> Dict[str, str]:
        """
        Renders the prompt templates with the provided variables.
        Falls back to English ('en') if the requested language is missing.
        """
        sys = self.system_prompt.get(lang, self.system_prompt.get("en", ""))
        dev = self.developer_prompt.get(lang, self.developer_prompt.get("en", ""))
        user = self.user_prompt_template.get(lang, self.user_prompt_template.get("en", ""))
        
        return {
            "system": sys.format(**kwargs),
            "developer": dev.format(**kwargs),
            "user": user.format(**kwargs)
        }


class PromptManager:
    """
    Manages all AI Brain prompt templates.
    Isolates prompt engineering from core business logic.
    Provides methods to fetch rendered prompts based on operational intent.
    """
    def __init__(self):
        self.templates: Dict[str, PromptTemplate] = {}
        self._initialize_templates()

    def _initialize_templates(self) -> None:
        """Registers all standardized templates required by the AI Brain."""
        
        # 1. Operational Decision
        op_dec = PromptTemplate("operational_decision")
        op_dec.add_language(
            "en",
            system="You are the core StadiumOS AI Brain. Your role is to analyze live stadium state and output structured operational decisions.",
            developer="CRITICAL INSTRUCTION: You MUST output valid JSON only. Do not wrap it in markdown block quotes (```json). Your response must strictly match this schema:\n{schema}",
            user="Current Stadium Context:\n{context}\n\nTask: Evaluate the operational state and provide actionable recommendations. Output strictly in JSON."
        )
        self.templates["operational_decision"] = op_dec

        # 2. Crowd Analysis
        crowd = PromptTemplate("crowd_analysis")
        crowd.add_language(
            "en",
            system="You are an expert crowd dynamics analyst for StadiumOS.",
            developer="CRITICAL INSTRUCTION: You MUST output valid JSON only conforming to this schema:\n{schema}",
            user="Crowd Data:\n{context}\n\nTask: Analyze congestion, identify specific bottlenecks, and suggest optimal gate redistribution or holding strategies."
        )
        self.templates["crowd_analysis"] = crowd

        # 3. Incident Summary
        inc_sum = PromptTemplate("incident_summary")
        inc_sum.add_language(
            "en",
            system="You are a crisis communication expert for StadiumOS.",
            developer="Provide a concise, professional executive summary. Output format constraints:\n{schema}",
            user="Recent Incidents:\n{context}\n\nTask: Provide a concise, high-level executive summary of all critical incidents and warnings."
        )
        self.templates["incident_summary"] = inc_sum

        # 4. SOP Generation
        sop = PromptTemplate("sop_generation")
        sop.add_language(
            "en",
            system="You are a Stadium Security Operations Manager.",
            developer="Ensure standard operating procedures strictly follow enterprise safety guidelines. Strict JSON schema:\n{schema}",
            user="Incident Context:\n{context}\n\nTask: Generate a precise, step-by-step Standard Operating Procedure (SOP) for resolving this specific incident."
        )
        self.templates["sop_generation"] = sop

        # 5. Multilingual Translation
        trans = PromptTemplate("multilingual_translation")
        trans.add_language(
            "en",
            system="You are a real-time stadium broadcast translator.",
            developer="You must output localized strings mapped properly in JSON. Schema:\n{schema}",
            user="Message:\n{message}\nTarget Language: {target_language}\n\nTask: Translate the broadcast message maintaining operational urgency."
        )
        self.templates["multilingual_translation"] = trans

        # 6. Weather Decision
        weather = PromptTemplate("weather_decision")
        weather.add_language(
            "en",
            system="You are a meteorological impact assessor for live stadium events.",
            developer="Output structured JSON decision matrices. Strict Schema:\n{schema}",
            user="Weather Data:\n{context}\n\nTask: Assess the current weather impact on the event and recommend immediate mitigations (e.g., roof closure, partial evacuation)."
        )
        self.templates["weather_decision"] = weather

        # 7. Threat Explanation
        threat = PromptTemplate("threat_explanation")
        threat.add_language(
            "en",
            system="You are a threat intelligence analyst for StadiumOS.",
            developer="Provide clear, calm, and highly objective threat analysis in structured JSON. Schema:\n{schema}",
            user="Threat Data:\n{context}\n\nTask: Explain the precise nature of the active threat and its potential operational impact radius."
        )
        self.templates["threat_explanation"] = threat

        # 8. Copilot Chat
        copilot = PromptTemplate("copilot_chat")
        copilot.add_language(
            "en",
            system="You are the StadiumOS Copilot ({agent_type} Agent).\nYou are an elite, highly professional AI Operations Commander.\nYour job is to answer the user's operational query using ONLY the provided telemetry context.\nNEVER act like a standard conversational chatbot. Always be direct, operational, and actionable.",
            developer="Analyze the user's query against the LIVE_CONTEXT and CHAT_HISTORY.\nGenerate a Situation Summary, Risk Level, Root Cause, and structured Recommend Actions.\nOutput strictly matching the requested JSON schema.",
            user="Query: {query}\n\nContext: {context}"
        )
        self.templates["copilot_chat"] = copilot

        # 9. Accessibility Assistance
        access = PromptTemplate("accessibility_assistance")
        access.add_language(
            "en",
            system="You are an accessibility and inclusion coordinator for StadiumOS.",
            developer="Focus on compliance, safety, and mobility for guests with disabilities. JSON schema:\n{schema}",
            user="Stadium State:\n{context}\n\nTask: Identify accessibility risks (e.g. elevator outages, crowded accessible gates) in the current state and suggest rapid support actions."
        )
        self.templates["accessibility_assistance"] = access

        # 10. Predictive Simulation
        sim = PromptTemplate("predictive_simulation")
        sim.add_language(
            "en",
            system="You are the StadiumOS Predictive Simulation Engine.\nYour job is to run hypothetical 'What-If' scenarios based on the live stadium state.",
            developer="CRITICAL INSTRUCTION: Analyze the DETECTED_SCENARIO and LIVE_STADIUM_STATE.\nGenerate a strict JSON response containing the PredictedState, RiskProfile, and Strategic Options (Option A, Option B, etc.).\nDo not invent numbers blindly; ensure they logically follow the current metrics.",
            user="Simulation Context:\n{context}\n\nTask: Generate the predictive simulation output."
        )
        self.templates["predictive_simulation"] = sim

    def get_prompt(self, template_name: str, lang: str = "en", **kwargs) -> Dict[str, str]:
        """
        Retrieves and renders a requested prompt template with variables safely injected.
        
        Args:
            template_name: The internal name of the prompt (e.g., 'operational_decision')
            lang: The target language code (default 'en')
            kwargs: Variables to inject into the template (context, schema, message, etc.)
            
        Returns:
            Dict containing 'system', 'developer', and 'user' string values.
        """
        if template_name not in self.templates:
            raise ValueError(f"Prompt template '{template_name}' not found.")
            
        # Ensure schema is properly stringified if passed as a native dict
        if 'schema' in kwargs and isinstance(kwargs['schema'], dict):
            kwargs['schema'] = json.dumps(kwargs['schema'], indent=2)
            
        # Provide safe default fallbacks for common required variables to prevent KeyError
        safe_kwargs = {
            'context': kwargs.get('context', '{}'),
            'schema': kwargs.get('schema', '{}'),
            'message': kwargs.get('message', ''),
            'target_language': kwargs.get('target_language', 'en'),
            'query': kwargs.get('query', ''),
            'agent_type': kwargs.get('agent_type', 'General')
        }
        
        # Merge any other custom kwargs not explicitly handled above
        for k, v in kwargs.items():
            if k not in safe_kwargs:
                safe_kwargs[k] = v
            
        return self.templates[template_name].render(lang=lang, **safe_kwargs)
