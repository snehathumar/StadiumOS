import streamlit as st
from backend.agents.evaluation.performance_analyzer import performance_analyzer
from backend.agents.evaluation.learning_memory import learning_memory
from backend.agents.evaluation.decision_logger import decision_logger

def render_analytics_dashboard():
    st.header("🧠 AI Evaluation & Learning", anchor=False)
    st.markdown("Monitor AI confidence drift, evaluate operational decisions, and inspect the continuous learning memory.")
    st.markdown("---")
    
    # Inject Mock Data for Demo Purposes if empty
    if performance_analyzer.total_decisions == 0:
        performance_analyzer.log_decision_outcome(True)
        performance_analyzer.log_decision_outcome(True)
        performance_analyzer.log_decision_outcome(False) # 66%
        performance_analyzer.log_prediction_outcome(True)
        performance_analyzer.log_prediction_outcome(True)
        learning_memory.add_lesson(
            context="Predictive Surge at Gate A",
            failure_reason="Predicted 20 min queue, actual was 45 min due to security bottleneck.",
            corrective_action="In future predictions involving Gate A, heavily weight the security screening throughput factor."
        )
        learning_memory.add_lesson(
            context="Agentic Deploy to Sector C",
            failure_reason="Deployed 5 guards, but crowd dispersed before arrival.",
            corrective_action="Always check realtime velocity of crowd movement before issuing deployment tasks."
        )

    metrics = performance_analyzer.get_metrics()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        with st.container(border=True):
            st.metric("Total AI Operations", f"{metrics['total_evaluations']}")
    with col2:
        with st.container(border=True):
            conf = metrics['current_confidence'] * 100
            st.metric("Internal AI Confidence", f"{conf:.1f}%")
    with col3:
        with st.container(border=True):
            st.metric("Decision Accuracy", f"{metrics['decision_accuracy']:.1f}%")
    with col4:
        with st.container(border=True):
            st.metric("Prediction Accuracy", f"{metrics['prediction_accuracy']:.1f}%")

    st.markdown("---")
    
    col_mem, col_log = st.columns([6, 4])
    
    with col_mem:
        st.markdown("### 📚 Long-Term Learning Memory")
        st.markdown("*(Rules injected dynamically into the AI Brain prompt)*")
        lessons = learning_memory.get_recent_lessons()
        for idx, lesson in enumerate(lessons):
            with st.expander(f"Lesson {idx+1}: {lesson['context']}", expanded=True):
                st.error(f"**Failed Because:** {lesson['avoid']}")
                st.success(f"**Learned Action:** {lesson['do_instead']}")

    with col_log:
        st.markdown("### 📝 Decision Audit Logger")
        logs = decision_logger.get_logs()
        if not logs:
            st.info("No decisions logged yet.")
        for log in logs[:5]:
            with st.container(border=True):
                st.markdown(f"**Source:** {log['source']} | **Time:** {log['timestamp'][11:19]}")
                st.markdown(f"**Decision:** {log['output']}")

if __name__ == "__main__":
    render_analytics_dashboard()
