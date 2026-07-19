import os
import shutil
import re
from pathlib import Path

def main():
    root = Path("d:/stadium os")
    
    # 1. Create New Directories
    dirs_to_create = [
        "assets", "backend", "frontend", "pages", "utils",
        "backend/stadium_state", "backend/event_engine", 
        "backend/threat_engine", "backend/ai_brain", 
        "backend/copilot", "backend/simulation", 
        "backend/agents", "backend/agents/agentic", "backend/agents/evaluation"
    ]
    for d in dirs_to_create:
        (root / d).mkdir(parents=True, exist_ok=True)
        
    # 2. Move Files
    moves = [
        ("core/stadium_state.py", "backend/stadium_state/stadium_state.py"),
        ("core/state.py", "backend/stadium_state/state.py"),
        ("core/models.py", "backend/event_engine/models.py"),
        ("core/event_bus.py", "backend/event_engine/event_bus.py"),
        ("core/store.py", "backend/event_engine/store.py"),
        ("core/bus.py", "backend/event_engine/bus.py"),
        ("core/logger.py", "utils/logger.py"),
        ("core/demo_simulator.py", "backend/event_engine/demo_simulator.py"),
        ("core/event_simulator.py", "backend/event_engine/event_simulator.py"),
        
        ("ai/copilot.py", "backend/copilot/copilot.py"),
    ]
    
    # Move security -> backend/threat_engine
    if (root / "security").exists():
        for f in (root / "security").iterdir():
            if f.is_file(): shutil.move(str(f), str(root / "backend/threat_engine" / f.name))
            
    # Move ai/agentic -> backend/agents/agentic
    if (root / "ai/agentic").exists():
        for f in (root / "ai/agentic").iterdir():
            if f.is_file(): shutil.move(str(f), str(root / "backend/agents/agentic" / f.name))
            
    # Move evaluation -> backend/agents/evaluation (except dashboard)
    if (root / "evaluation").exists():
        for f in (root / "evaluation").iterdir():
            if f.is_file():
                if f.name == "analytics_dashboard.py":
                    shutil.move(str(f), str(root / "pages/4_AI_Analytics.py"))
                else:
                    shutil.move(str(f), str(root / "backend/agents/evaluation" / f.name))
                    
    # Move rest of ai -> backend/ai_brain
    if (root / "ai").exists():
        for f in (root / "ai").iterdir():
            if f.is_file(): shutil.move(str(f), str(root / "backend/ai_brain" / f.name))
            
    # Move simulation -> backend/simulation
    if (root / "simulation").exists():
        for f in (root / "simulation").iterdir():
            if f.is_file(): shutil.move(str(f), str(root / "backend/simulation" / f.name))
            
    # Move ui -> frontend and pages
    if (root / "ui").exists():
        for f in (root / "ui").iterdir():
            if f.is_file():
                if f.name == "app.py":
                    shutil.move(str(f), str(root / "app.py"))
                elif f.name == "copilot_view.py":
                    shutil.move(str(f), str(root / "pages/1_Copilot.py"))
                elif f.name == "agentic_view.py":
                    shutil.move(str(f), str(root / "pages/2_Agentic_Ops.py"))
                elif f.name == "simulation_view.py":
                    shutil.move(str(f), str(root / "pages/3_Predictive_Simulation.py"))
                elif f.name in ["theme.py", "layout.py"]:
                    shutil.move(str(f), str(root / "frontend" / f.name))
        # Move ui subdirs if any (like components, charts)
        for d in ["components", "charts", "assets"]:
            if (root / "ui" / d).exists():
                shutil.move(str(root / "ui" / d), str(root / "frontend" / d))

    # Apply specific moves
    for src, dst in moves:
        src_path = root / src
        if src_path.exists():
            shutil.move(str(src_path), str(root / dst))
            
    # 3. Clean up old dirs
    for d in ["core", "security", "ai", "simulation", "evaluation", "ui", "simulator"]:
        if (root / d).exists():
            shutil.rmtree(str(root / d), ignore_errors=True)

    # 4. Search and Replace imports
    import_replacements = {
        r"from core\.stadium_state": "from backend.stadium_state.stadium_state",
        r"import core\.stadium_state": "import backend.stadium_state.stadium_state",
        r"from core\.state": "from backend.stadium_state.state",
        r"import core\.state": "import backend.stadium_state.state",
        r"from core\.models": "from backend.event_engine.models",
        r"from core\.event_bus": "from backend.event_engine.event_bus",
        r"from core\.store": "from backend.event_engine.store",
        r"from core\.bus": "from backend.event_engine.bus",
        r"from core\.logger": "from utils.logger",
        r"from core\.demo_simulator": "from backend.event_engine.demo_simulator",
        r"from core\.event_simulator": "from backend.event_engine.event_simulator",
        
        r"from security\.": "from backend.threat_engine.",
        r"import security\.": "import backend.threat_engine.",
        
        r"from ai\.copilot": "from backend.copilot.copilot",
        r"import ai\.copilot": "import backend.copilot.copilot",
        
        r"from ai\.agentic\.": "from backend.agents.agentic.",
        r"import ai\.agentic\.": "import backend.agents.agentic.",
        
        r"from evaluation\.analytics_dashboard": "from pages.4_AI_Analytics",
        
        r"from evaluation\.": "from backend.agents.evaluation.",
        r"import evaluation\.": "import backend.agents.evaluation.",
        
        r"from ai\.": "from backend.ai_brain.",
        r"import ai\.": "import backend.ai_brain.",
        
        r"from simulation\.": "from backend.simulation.",
        r"import simulation\.": "import backend.simulation.",
        
        r"from ui\.theme": "from frontend.theme",
        r"from ui\.layout": "from frontend.layout",
        r"from ui\.components": "from frontend.components",
        r"from ui\.charts": "from frontend.charts",
    }
    
    for filepath in root.rglob("*.py"):
        try:
            content = filepath.read_text(encoding="utf-8")
            new_content = content
            for pattern, repl in import_replacements.items():
                new_content = re.sub(pattern, repl, new_content)
            if new_content != content:
                filepath.write_text(new_content, encoding="utf-8")
        except Exception as e:
            print(f"Error processing {filepath}: {e}")
            
    print("Refactoring complete.")

if __name__ == "__main__":
    main()
    import sys
    sys.exit(0)
