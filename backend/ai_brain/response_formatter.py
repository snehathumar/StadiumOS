from typing import Dict, Any
from backend.ai_brain.models import StadiumBrainResponse

class ResponseFormatter:
    """
    Converts raw Pydantic AI models into clean, UI-ready dictionaries or markdown strings.
    Ensures the Streamlit UI doesn't have to parse complex data objects directly.
    """
    
    @staticmethod
    def to_markdown(response: StadiumBrainResponse) -> str:
        """Transforms a structured AI decision into a beautiful Markdown report."""
        md = f"### 📊 Situation Summary\n{response.summary}\n\n"
        
        # Color code risk
        color = "🟢" if response.risk_level == "NOMINAL" else ("🟠" if response.risk_level == "WARNING" else "🔴")
        md += f"**Risk Level:** {color} `{response.risk_level}`  |  "
        md += f"**Confidence Score:** {response.confidence * 100:.1f}%\n\n"
        
        md += "### ⚡ Recommended Actions\n"
        if response.recommended_actions:
            # Sort by rank strictly
            sorted_actions = sorted(response.recommended_actions, key=lambda x: x.rank)
            for action in sorted_actions:
                md += f"{action.rank}. **[{action.urgency}]** (`{action.target_system}`) {action.action}\n"
        else:
            md += "*No immediate actions required based on current context.*\n"
            
        md += f"\n### 🧠 Reasoning\n{response.reasoning}\n"
        
        return md
        
    @staticmethod
    def to_ui_dict(response: StadiumBrainResponse) -> Dict[str, Any]:
        """Provides a safe, raw dictionary for custom UI rendering."""
        return response.model_dump()
