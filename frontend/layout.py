import streamlit as st
from typing import Dict, Any, List
from frontend.components.metric_card import render_metric_card
from frontend.components.status_card import render_status_card
from frontend.charts.crowd_chart import render_crowd_chart
from frontend.charts.gate_chart import render_gate_chart
from frontend.components.alert_panel import render_incident_timeline
from backend.event_engine.models import StadiumEvent

def render_wireframe_dashboard(state_data: Dict[str, Any], events: List[StadiumEvent]) -> None:
    """
    Renders the exact StadiumOS dashboard layout based on the approved wireframe.
    """
    # ------------------------------------------------------------
    # Row 1: Header
    # ------------------------------------------------------------
    st.markdown("<h1 style='text-align: center; color: #ffffff;'>🏟 StadiumOS</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #8b949e; font-size: 1.2rem; font-weight: 500;'>One AI. Every Stadium Decision.</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    # ------------------------------------------------------------
    # Row 2: Primary Health Indicators (4 Columns)
    # ------------------------------------------------------------
    # Compute global health
    global_health = "GOOD"
    for cat, locations in state_data.items():
        for loc, state in locations.items():
            if state.health == "CRITICAL":
                global_health = "CRITICAL"
            elif state.health == "WARNING" and global_health != "CRITICAL":
                global_health = "WARNING"
                
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_metric_card("Stadium Health", "ONLINE", global_health, "🏟️")
    with c2:
        _render_card_from_state("WEATHER", "Weather", "🌦️", state_data)
    with c3:
        _render_card_from_state("CROWD", "Crowd", "👥", state_data)
    with c4:
        # Mock Threat Level
        render_metric_card("Threat", "SECURE", "GOOD", "🔴" if global_health == "CRITICAL" else "🛡️")

    st.markdown("---")
    
    # ------------------------------------------------------------
    # Row 3: Charts & Timeline (3 Columns)
    # ------------------------------------------------------------
    ch1, ch2, ch3 = st.columns(3)
    with ch1:
        render_crowd_chart(events)
    with ch2:
        render_gate_chart(events)
    with ch3:
        # Medical Pie chart was here previously, can be replaced by threat_chart or timeline later
        st.info("Placeholder for 3rd chart")
        
    st.markdown("---")

    # ------------------------------------------------------------
    # Row 4: Secondary Subsystem Cards (4 Columns)
    # ------------------------------------------------------------
    b1, b2, b3, b4 = st.columns(4)
    with b1:
        _render_card_from_state("MEDICAL", "Medical", "🚑", state_data)
    with b2:
        _render_card_from_state("NETWORK", "Network", "📡", state_data)
    with b3:
        _render_card_from_state("IOT", "IoT", "🔌", state_data)
    with b4:
        _render_card_from_state("TICKET", "Ticket", "🎟️", state_data)
        
    st.markdown("---")

    # ------------------------------------------------------------
    # Row 5: Recent Alerts
    # ------------------------------------------------------------
    render_incident_timeline(events)

def _render_card_from_state(category: str, title: str, icon: str, state_data: Dict[str, Any]) -> None:
    """Helper to safely extract and render a card from the global state dict without logic calculation."""
    if category in state_data and state_data[category]:
        # Get the first available location/source for summary representation
        first_loc = list(state_data[category].keys())[0]
        data = state_data[category][first_loc]
        
        # Display the primary status text directly from backend
        value = str(data.status)
        
        render_metric_card(
            title=title,
            value=value,
            health=data.health,
            icon=icon,
            last_updated=data.last_updated.strftime("%H:%M:%S")
        )
    else:
        render_metric_card(title=title, value="NO DATA", health="UNKNOWN", icon=icon)
