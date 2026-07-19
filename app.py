import streamlit as st
import time
import sys
import os

# Inject backend path for independent UI execution
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.stadium_state.stadium_state import stadium_state_aggregator
from backend.event_engine.store import event_store
from frontend.theme import apply_theme
from frontend.layout import render_wireframe_dashboard

def main():
    """
    Main Streamlit Application Entrypoint.
    Functions as the Dashboard root page in the Multi-Page setup.
    """
    st.set_page_config(
        page_title="StadiumOS",
        page_icon="🏟️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # 1. Apply UI Theme
    apply_theme()
    
    st.sidebar.markdown("---")
    st.sidebar.info("Select a module above to navigate.")
    
    # 2. Fetch Data (Dependency Inversion)
    snapshot = stadium_state_aggregator.get_current_state()
    recent_events = event_store.get_recent_events(limit=200)
    
    # 3. Route Rendering
    render_wireframe_dashboard(snapshot.subsystems, recent_events)
        
    # 4. Auto-Refresh Loop
    time.sleep(2)
    st.rerun()

if __name__ == "__main__":
    main()
