import streamlit as st
from typing import List
from backend.event_engine.models import StadiumEvent

def render_incident_timeline(events: List[StadiumEvent]):
    """Visual Timeline component showing recent events"""
    if not events:
        st.info("No active incidents.")
        return
        
    for evt in events[:5]:
        with st.container(border=True):
            st.markdown(f"**[{evt.severity.value}] {evt.category.value}** - {evt.location}")
            st.markdown(f"_{evt.description}_")
