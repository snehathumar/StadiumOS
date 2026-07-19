import streamlit as st

def apply_theme() -> None:
    """
    Injects ultra-premium custom CSS for a Palantir/Tesla/Apple inspired Glassmorphism UI.
    """
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    :root {
        --bg-color: #0b0f19;
        --card-bg: rgba(16, 22, 35, 0.65);
        --glass-border: rgba(255, 255, 255, 0.08);
        --glass-glow: rgba(56, 189, 248, 0.15);
        --text-primary: #f8fafc;
        --text-secondary: #94a3b8;
        
        --good-glow: rgba(34, 197, 94, 0.4);
        --warn-glow: rgba(234, 179, 8, 0.4);
        --crit-glow: rgba(239, 68, 68, 0.4);
    }
    
    .stApp {
        background-color: var(--bg-color);
        background-image: 
            radial-gradient(circle at 15% 50%, rgba(56, 189, 248, 0.03), transparent 25%),
            radial-gradient(circle at 85% 30%, rgba(168, 85, 247, 0.03), transparent 25%);
        color: var(--text-primary);
        font-family: 'Inter', sans-serif;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Premium Glassmorphism */
    .glass-card {
        background: var(--card-bg);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid var(--glass-border);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        position: relative;
        overflow: hidden;
    }
    
    .glass-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
    }
    
    .glass-card:hover {
        transform: translateY(-3px) scale(1.01);
        box-shadow: 0 12px 30px rgba(0,0,0,0.5), 0 0 20px var(--glass-glow);
        border-color: rgba(255, 255, 255, 0.15);
    }
    
    .card-title {
        font-size: 0.85rem;
        font-weight: 600;
        color: var(--text-secondary);
        margin-bottom: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        display: flex;
        align-items: center;
    }
    
    .card-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: var(--text-primary);
        background: linear-gradient(to right, #ffffff, #94a3b8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .card-meta {
        font-size: 0.75rem;
        color: var(--text-secondary);
        margin-top: 1rem;
        border-top: 1px solid rgba(255,255,255,0.05);
        padding-top: 0.5rem;
    }
    
    .health-indicator {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        margin-right: 12px;
    }
    
    .health-GOOD { background-color: #22c55e; box-shadow: 0 0 10px var(--good-glow); }
    .health-WARNING { background-color: #eab308; box-shadow: 0 0 10px var(--warn-glow); }
    .health-CRITICAL { background-color: #ef4444; box-shadow: 0 0 10px var(--crit-glow); }
    .health-UNKNOWN { background-color: #64748b; }
    
    </style>
    """, unsafe_allow_html=True)
