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
    Renders a reusable, glassmorphic metric card.
    """
    if health not in ["GOOD", "WARNING", "CRITICAL"]:
        health = "UNKNOWN"
        
    trend_html = f"<span style='float:right; font-size: 0.8rem;'>{trend}</span>" if trend else ""
    meta_html = f"<div class='card-meta'>Last updated: {last_updated}</div>" if last_updated else ""
    
    html = f"""
    <div class="glass-card">
        <div class="card-title">
            <span class="health-indicator health-{health}"></span>
            {icon} {title}
            {trend_html}
        </div>
        <div class="card-value">{value}</div>
        {meta_html}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
