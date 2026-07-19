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
        font=dict(color="#8b949e", family="-apple-system, BlinkMacSystemFont, sans-serif"),
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)", zeroline=False),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig

def render_crowd_chart(events: List[StadiumEvent]) -> None:
    crowd_events = [e for e in events if e.category.value == "CROWD"]
    if not crowd_events:
        st.info("No crowd data.")
        return
        
    df = pd.DataFrame([{
        "Time": e.timestamp,
        "Location": e.location,
        "Occupancy": e.metrics.get("occupancy_percentage", 0)
    } for e in crowd_events])
    
    if df.empty: return
        
    fig = px.area(
        df, x="Time", y="Occupancy", color="Location",
        title="Crowd Occupancy Density",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    st.plotly_chart(_apply_plotly_dark_theme(fig), use_container_width=True)
