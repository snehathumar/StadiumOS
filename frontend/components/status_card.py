import streamlit as st
from frontend.components.metric_card import render_metric_card

def render_status_card(title: str, status_value: str, global_health: str, icon: str) -> None:
    """
    Specifically renders high-level global status cards using the metric card base.
    """
    render_metric_card(
        title=title,
        value=status_value,
        health=global_health,
        icon=icon,
        last_updated="Just now"
    )
