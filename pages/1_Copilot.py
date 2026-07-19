import streamlit as st
from backend.copilot.copilot import StadiumCopilot
from backend.event_engine.demo_simulator import demo_simulator
from backend.stadium_state.stadium_state import stadium_state_aggregator

def initialize_copilot():
    """Initializes the AI copilot in the Streamlit session state."""
    if 'copilot' not in st.session_state:
        st.session_state.copilot = StadiumCopilot()
    if 'messages' not in st.session_state:
        st.session_state.messages = []

def _render_demo_controls():
    """Sidebar buttons to inject crisis states for demonstration."""
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🧪 Demo Scenarios")
    
    if st.sidebar.button("🚨 1. Gate Overcrowding"):
        demo_simulator.reset()
        demo_simulator.inject_scenario_1_overcrowding()
        st.sidebar.success("Scenario 1 Injected!")
        
    if st.sidebar.button("🛡️ 2. Security Threat"):
        demo_simulator.reset()
        demo_simulator.inject_scenario_2_security_threat()
        st.sidebar.success("Scenario 2 Injected!")
        
    if st.sidebar.button("🔮 3. Predictive Surge"):
        demo_simulator.reset()
        demo_simulator.inject_scenario_3_predictive_simulation()
        st.sidebar.success("Scenario 3 Injected!")
        
    if st.sidebar.button("🔄 Reset State"):
        demo_simulator.reset()
        # Clean session memory
        if 'copilot' in st.session_state:
            st.session_state.copilot.memory_history = []
        st.session_state.messages = []
        st.sidebar.info("State Reset.")

def render_copilot_view():
    """Renders the dual-pane premium Copilot interface."""
    initialize_copilot()
    _render_demo_controls()
    
    # Header
    st.header("🤖 StadiumOS Copilot", anchor=False)
    st.markdown("Your AI Operations Assistant. Ask natural language queries to evaluate live stadium context.")
    st.markdown("---")
    
    # 60/40 Split Layout
    col_chat, col_context = st.columns([6, 4])
    
    with col_chat:
        st.markdown("### Conversation")
        
        # Render Chat History
        chat_container = st.container(height=500)
        with chat_container:
            for msg in st.session_state.messages:
                with st.chat_message(msg["role"]):
                    if msg["role"] == "user":
                        st.markdown(msg["content"])
                    else:
                        # Render rich AI response
                        resp = msg["content"]
                        
                        # Risk Badge
                        color = "green"
                        if resp.risk_level == "CRITICAL": color = "red"
                        elif resp.risk_level == "HIGH": color = "orange"
                        elif resp.risk_level == "MEDIUM": color = "yellow"
                        
                        st.markdown(f"**Risk Level:** :{color}[{resp.risk_level}]")
                        st.markdown(f"**Summary:** {resp.situation_summary}")
                        
                        if resp.root_cause and resp.root_cause != "N/A":
                            st.markdown(f"**Root Cause:** {resp.root_cause}")
                            
                        st.markdown("#### Recommended Actions:")
                        for act in resp.recommended_actions:
                            st.markdown(f"**{act.rank}. {act.action}** (Priority {act.priority})")
                            st.markdown(f"- 📍 Location: {act.location}")
                            st.markdown(f"- 👥 Resources: {act.resource_required}")
                            st.markdown(f"- 📈 Impact: {act.expected_result}")
                        
                        st.info(f"**Overall Impact:** {resp.expected_impact}")
        
        # Chat Input handler
        try:
            query = st.chat_input("Ask Copilot a question (e.g., 'What is the risk of a crush at Gate A?')")
            if query:
                import re
                from backend.ai_brain.ai_manager import AIManager
                from backend.ai_brain.decision_logger import decision_logger
                
                # Strict input sanitization
                sanitized_query = re.sub(r'[^a-zA-Z0-9 ?.,!-]', '', query)
                
                st.session_state.messages.append({"role": "user", "content": sanitized_query})
                with chat_container:
                    with st.chat_message("user"):
                        st.write(sanitized_query)
                        
                with chat_container:
                    with st.chat_message("assistant"):
                        with st.spinner("Analyzing live context..."):
                            try:
                                ai_manager = AIManager()
                                response = ai_manager.execute_brain_task(
                                    template_name="copilot",
                                    user_prompt=sanitized_query
                                )
                                
                                st.write(response.summary)
                                
                                # Log decision automatically
                                decision_logger.log_decision(
                                    context_snapshot=stadium_state_aggregator.get_current_state(),
                                    scenario=sanitized_query,
                                    ai_recommendation=response,
                                    human_override=None
                                )
                                
                                st.session_state.messages.append({"role": "assistant", "content": response})
                                st.rerun()
                            except Exception as e:
                                error_msg = "Error analyzing context. Please try again."
                                st.error(error_msg)
        except Exception as general_e:
            st.error("An unexpected error occurred in the Copilot UI. Please check the system logs.")

    with col_context:
        st.markdown("### 📡 Live Stadium Context")
        st.caption("Data streams visible to Copilot")
        
        # Render a raw dump or a visual representation of current context
        snapshot = stadium_state_aggregator.get_current_state()
        
        # Show Critical Subsystems
        criticals = []
        warnings = []
        for cat, locations in snapshot.subsystems.items():
            for loc, state in locations.items():
                if state.health == "CRITICAL":
                    criticals.append(f"{cat} - {loc}: {state.status}")
                elif state.health == "WARNING":
                    warnings.append(f"{cat} - {loc}: {state.status}")
                    
        if criticals:
            st.error("**CRITICAL ALERTS:**\n\n" + "\n".join(criticals))
        if warnings:
            st.warning("**WARNINGS:**\n\n" + "\n".join(warnings))
        if not criticals and not warnings:
            st.success("All systems nominal.")
            
        st.markdown("#### Raw Telemetry Payload")
        with st.expander("View JSON Context"):
            # Mock dump of what context_builder sees
            from backend.ai_brain.context_builder import ContextBuilder
            cb = ContextBuilder()
            st.json(cb.build_context())

if __name__ == "__main__":
    render_copilot_view()
