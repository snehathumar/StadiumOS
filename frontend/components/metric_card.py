import streamlit as st
from typing import Optional

def render_metric_card(
    title: str,
    value: str,
    health: str,
    icon: str = "",
    trend: Optional[str] = None,
    last_updated: Optional[str] = None
) -> None:
    """
    Renders a native metric card to ensure maximum accessibility and security.
    """
    label = f"{icon} {title}"
    st.metric(label=label, value=value, delta=trend)
