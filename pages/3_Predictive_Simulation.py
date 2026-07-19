import streamlit as st
from backend.simulation.simulation_service import simulation_service
from backend.simulation.models import SimulationResult

def render_simulation_view():
    st.header("🔮 Predictive Simulation Engine", anchor=False)
    st.markdown("Run hypothetical scenarios to predict future impact and generate preventive strategies.")
    st.markdown("---")
    
    # Scenario Input
    col_input, col_btn = st.columns([8, 2])
    with col_input:
        query = st.text_input("Describe the hypothetical scenario:", placeholder="e.g. What happens if 20,000 more fans arrive?")
    with col_btn:
        st.write("")
        run_sim = st.button("🚀 Run Simulation", type="primary")
        
    if run_sim and query:
        with st.spinner("Executing What-If Analysis..."):
            try:
                result: SimulationResult = simulation_service.run_simulation(query)
                st.session_state.last_sim = result
            except Exception as e:
                st.error(f"Simulation Failed: {str(e)}")
                
    if 'last_sim' in st.session_state:
        result: SimulationResult = st.session_state.last_sim
        
        st.markdown(f"### 📍 Scenario: `{result.scenario}`")
        
        # State Comparison
        col_cur, col_pred, col_risk = st.columns(3)
        with col_cur:
            with st.container(border=True):
                st.markdown("#### ⏳ Current State")
                st.markdown(f"*{result.current_state_summary}*")
        
        with col_pred:
            with st.container(border=True):
                st.markdown("#### 🔮 Predicted State")
                st.markdown(f"**Attendance:** {result.predicted_state.attendance}")
                for k, v in result.predicted_state.key_metrics.items():
                    st.markdown(f"**{k}:** {v}")
                    
        with col_risk:
            with st.container(border=True):
                st.markdown("#### ⚠️ Future Risk Profile")
                
                # Helper for color mapping
                def get_color(risk: str):
                    if risk == "CRITICAL": return "red"
                    if risk == "HIGH": return "orange"
                    if risk == "MEDIUM": return "yellow"
                    return "green"
                    
                overall_color = get_color(result.risk.overall_risk)
                st.markdown(f"**Overall Risk:** :{overall_color}[{result.risk.overall_risk}]")
                st.markdown(f"- Crowd: :{get_color(result.risk.crowd_risk)}[{result.risk.crowd_risk}]")
                st.markdown(f"- Security: :{get_color(result.risk.security_risk)}[{result.risk.security_risk}]")
                st.markdown(f"- Operations: :{get_color(result.risk.operational_risk)}[{result.risk.operational_risk}]")
                st.markdown(f"- Medical: :{get_color(result.risk.medical_risk)}[{result.risk.medical_risk}]")

        st.markdown("---")
        st.markdown("### 🛠️ Strategic Options Analysis")
        
        # Render Options side-by-side
        num_options = len(result.alternative_plans)
        if num_options > 0:
    try:
        if run_sim and query:
            # Strict input sanitization
            sanitized_query = re.sub(r'[^a-zA-Z0-9 ?.,!-]', '', query)
            
            with st.spinner("Executing What-If Analysis..."):
                try:
                    result: SimulationResult = simulation_service.run_simulation(sanitized_query)
                    st.session_state.last_sim = result
                except Exception as e:
                    st.error(f"Simulation Failed: {str(e)}")
                    
        if 'last_sim' in st.session_state:
            result: SimulationResult = st.session_state.last_sim
            
            st.markdown(f"### 📍 Scenario: `{result.scenario}`")
            
            # State Comparison
            col_cur, col_pred, col_risk = st.columns(3)
            with col_cur:
                with st.container(border=True):
                    st.markdown("#### ⏳ Current State")
                    st.markdown(f"*{result.current_state_summary}*")
            
            with col_pred:
                with st.container(border=True):
                    st.markdown("#### 🔮 Predicted State")
                    st.markdown(f"**Attendance:** {result.predicted_state.attendance}")
                    for k, v in result.predicted_state.key_metrics.items():
                        st.markdown(f"**{k}:** {v}")
                        
            with col_risk:
                with st.container(border=True):
                    st.markdown("#### ⚠️ Future Risk Profile")
                    
                    # Helper for color mapping
                    def get_color(risk: str):
                        if risk == "CRITICAL": return "red"
                        if risk == "HIGH": return "orange"
                        if risk == "MEDIUM": return "yellow"
                        return "green"
                        
                    overall_color = get_color(result.risk.overall_risk)
                    st.markdown(f"**Overall Risk:** :{overall_color}[{result.risk.overall_risk}]")
                    st.markdown(f"- Crowd: :{get_color(result.risk.crowd_risk)}[{result.risk.crowd_risk}]")
                    st.markdown(f"- Security: :{get_color(result.risk.security_risk)}[{result.risk.security_risk}]")
                    st.markdown(f"- Operations: :{get_color(result.risk.operational_risk)}[{result.risk.operational_risk}]")
                    st.markdown(f"- Medical: :{get_color(result.risk.medical_risk)}[{result.risk.medical_risk}]")

            st.markdown("---")
            st.markdown("### 🛠️ Strategic Options Analysis")
            
            # Render Options side-by-side
            num_options = len(result.alternative_plans)
            if num_options > 0:
                cols = st.columns(num_options)
                for idx, opt in enumerate(result.alternative_plans):
                    with cols[idx]:
                        with st.container(border=True):
                            st.markdown(f"#### {opt.option_name}")
                            st.markdown(f"**Risk Level:** :{get_color(opt.risk_level)}[{opt.risk_level}]")
                            st.markdown(f"**Expected Delay:** {opt.expected_delay}")
                            st.markdown(f"**Required Resources:** {opt.required_resources}")
                            st.markdown("**Actions:**")
                            for a in opt.actions:
                                st.markdown(f"- {a}")
            else:
                st.info("No alternative plans generated.")
                
            st.markdown("---")
            st.markdown("### 🧠 AI Reasoning")
            st.info(result.reasoning)
    except Exception as general_e:
        st.error("An unexpected error occurred in the Simulation Engine.")

if __name__ == "__main__":
    render_simulation_view()
