import streamlit as st
from backend.agents.agentic.planner import PlannerAgent
from backend.agents.agentic.executor import executor_engine
from backend.agents.agentic.audit import audit_store

def initialize_agentic_state():
    if 'planner' not in st.session_state:
        st.session_state.planner = PlannerAgent()
    if 'current_plan' not in st.session_state:
        st.session_state.current_plan = None
    if 'operator_goal' not in st.session_state:
        st.session_state.operator_goal = ""

def render_agentic_view():
    initialize_agentic_state()
    
    st.header("⚡ Agentic Operations Coordinator", anchor=False)
    st.markdown("Direct multiple AI agents to execute operational goals safely via tool calling.")
    st.markdown("---")
    
    col_main, col_audit = st.columns([7, 3])
    
    with col_main:
        # Goal Input
        goal = st.text_input("Operator Goal", placeholder="e.g., Clear congestion at Gate C and notify security...")
        
        if st.button("🧠 Generate Execution Plan"):
            if goal:
                with st.spinner("Planner Agent is orchestrating tasks..."):
                    st.session_state.operator_goal = goal
                    # Generate the Plan
                    plan = st.session_state.planner.create_plan(goal)
                    st.session_state.current_plan = plan
                    st.rerun()
            else:
                st.warning("Please enter a goal.")
                
        # Render Active Plan
        if st.session_state.current_plan:
            plan = st.session_state.current_plan
            
            st.markdown(f"### 📋 Execution Plan: `{plan.plan_id}`")
            status_color = "yellow"
            if plan.status == "SUCCESS": status_color = "green"
            elif plan.status == "FAILED": status_color = "red"
            st.markdown(f"**Status:** :{status_color}[{plan.status}]")
            
            # Render Tasks and Tools
            for idx, task in enumerate(plan.tasks):
                with st.expander(f"Task {idx+1}: {task.description} ({task.status})", expanded=True):
                    st.markdown(f"**Assigned Agent:** `{task.assigned_agent.value}`")
                    st.markdown("**Tool Calls:**")
                    
                    if not task.tool_calls:
                        st.info("No tools required.")
                    
                    for call in task.tool_calls:
                        st.code(f"{call.tool_name}({call.arguments})", language="python")
                        st.markdown(f"> *Reasoning: {call.reasoning}*")
                        
                    if task.result_message:
                        st.markdown(f"**Result:** {task.result_message}")
            
            st.markdown("---")
            
            # Approval Gate
            if plan.status == "AWAITING_APPROVAL":
                st.warning("⚠️ **Human-in-the-Loop Required:** Review the tool calls above. Do you authorize this plan?")
                col_y, col_n = st.columns(2)
                with col_y:
                    if st.button("✅ APPROVE & EXECUTE", type="primary"):
                        plan.status = "APPROVED"
                        with st.spinner("Executing Tools..."):
                            executor_engine.execute_plan(plan, st.session_state.operator_goal)
                        st.rerun()
                with col_n:
                    if st.button("❌ REJECT"):
                        st.session_state.current_plan = None
                        st.rerun()

    with col_audit:
        st.markdown("### 📜 Audit Log")
        st.caption("Immutable record of all agentic operations.")
        
        logs = audit_store.get_logs()
        if not logs:
            st.info("No operations executed yet.")
        with st.expander("📋 View Immutable Audit Log"):
            for entry in list(reversed(audit_store.logs)):
                st.code(f"[{entry.timestamp}] {entry.operator_request} -> {entry.execution_status}")

if __name__ == "__main__":
    render_agentic_view()
