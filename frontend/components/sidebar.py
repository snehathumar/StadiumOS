import streamlit as st

def render_sidebar() -> str:
    """
    Renders the visual sidebar component.
    Returns the currently selected page name.
    """
    with st.sidebar:
        st.title("🏟️ StadiumOS")
        st.markdown("<p style='color:#8b949e; font-size:0.8rem; margin-top:-15px;'>One AI. Every Stadium Decision.</p>", unsafe_allow_html=True)
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
        st.markdown("<div style='text-align: center; color:#8b949e; font-size: 0.7rem;'>System: ONLINE</div>", unsafe_allow_html=True)
            
        return st.session_state.current_page
