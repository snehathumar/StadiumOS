import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import List
from backend.event_engine.models import StadiumEvent

def _apply_plotly_dark_theme(fig: go.Figure) -> go.Figure:
    fig.update_layout(
        template="plotly_dark",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=40, b=10),
        font=dict(color="#8b949e", family="-apple-system, BlinkMacSystemFont, sans-serif")
    )
    return fig

def render_weather_chart(events: List[StadiumEvent]) -> None:
    """Placeholder for weather visualization"""
    st.info("Weather chart placeholder")
