import streamlit as st

def render_sidebar() -> str:
    """
    Renders the visual sidebar component.
    Returns the currently selected page name.
    """
    with st.sidebar:
        st.header("🏟 StadiumOS")
        st.caption("One AI. Every Stadium Decision.")
        st.markdown("---")
        
        if 'current_page' not in st.session_state:
            st.session_state.current_page = "Dashboard"
            
        def switch_page(page: str):
            st.session_state.current_page = page
            
        st.button("📊 Operations Dashboard", use_container_width=True, on_click=switch_page, args=("Dashboard",))
        st.button("🧠 AI Brain", use_container_width=True, on_click=switch_page, args=("AI Brain",))
        st.button("🛡️ Threat Engine", use_container_width=True, on_click=switch_page, args=("Threat Engine",))
        st.button("🤖 Copilot", use_container_width=True, on_click=switch_page, args=("Copilot",))
        
        st.markdown("---")
        st.write("System: ONLINE")
            
        return st.session_state.current_page
