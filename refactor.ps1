$root = "d:\stadium os"
cd $root

# 1. Create directories
$dirs = @("assets", "backend", "frontend", "pages", "utils", "backend\stadium_state", "backend\event_engine", "backend\threat_engine", "backend\ai_brain", "backend\copilot", "backend\simulation", "backend\agents", "backend\agents\agentic", "backend\agents\evaluation")
foreach ($d in $dirs) {
    if (!(Test-Path $d)) { New-Item -ItemType Directory -Path $d -Force | Out-Null }
}

# 2. Move files mapped individually
$moves = @(
    @("core\stadium_state.py", "backend\stadium_state\"),
    @("core\state.py", "backend\stadium_state\"),
    @("core\models.py", "backend\event_engine\"),
    @("core\event_bus.py", "backend\event_engine\"),
    @("core\store.py", "backend\event_engine\"),
    @("core\bus.py", "backend\event_engine\"),
    @("core\demo_simulator.py", "backend\event_engine\"),
    @("core\event_simulator.py", "backend\event_engine\"),
    @("core\logger.py", "utils\"),
    @("ai\copilot.py", "backend\copilot\"),
    @("evaluation\analytics_dashboard.py", "pages\4_AI_Analytics.py"),
    @("ui\app.py", "app.py"),
    @("ui\copilot_view.py", "pages\1_Copilot.py"),
    @("ui\agentic_view.py", "pages\2_Agentic_Ops.py"),
    @("ui\simulation_view.py", "pages\3_Predictive_Simulation.py")
)
foreach ($m in $moves) {
    if (Test-Path $m[0]) { Move-Item -Path $m[0] -Destination $m[1] -Force }
}

# Move block directories
if (Test-Path "security\*") { Move-Item -Path "security\*" -Destination "backend\threat_engine\" -Force }
if (Test-Path "ai\agentic\*") { Move-Item -Path "ai\agentic\*" -Destination "backend\agents\agentic\" -Force }
if (Test-Path "evaluation\*") { Move-Item -Path "evaluation\*" -Destination "backend\agents\evaluation\" -Force }
if (Test-Path "ai\*") { Move-Item -Path "ai\*" -Destination "backend\ai_brain\" -Force }
if (Test-Path "simulation\*") { Move-Item -Path "simulation\*" -Destination "backend\simulation\" -Force }

if (Test-Path "ui\theme.py") { Move-Item -Path "ui\theme.py" -Destination "frontend\" -Force }
if (Test-Path "ui\layout.py") { Move-Item -Path "ui\layout.py" -Destination "frontend\" -Force }
if (Test-Path "ui\components") { Move-Item -Path "ui\components" -Destination "frontend\" -Force }
if (Test-Path "ui\charts") { Move-Item -Path "ui\charts" -Destination "frontend\" -Force }
if (Test-Path "ui\assets") { Move-Item -Path "ui\assets" -Destination "frontend\" -Force }

# Clean up
$old_dirs = @("core", "security", "ai", "simulation", "evaluation", "ui", "simulator")
foreach ($d in $old_dirs) {
    if (Test-Path $d) { Remove-Item -Path $d -Recurse -Force }
}

# Regex replace
$replacements = @{
    "from core\.stadium_state" = "from backend.stadium_state.stadium_state";
    "import core\.stadium_state" = "import backend.stadium_state.stadium_state";
    "from core\.state" = "from backend.stadium_state.state";
    "import core\.state" = "import backend.stadium_state.state";
    "from core\.models" = "from backend.event_engine.models";
    "from core\.event_bus" = "from backend.event_engine.event_bus";
    "from core\.store" = "from backend.event_engine.store";
    "from core\.bus" = "from backend.event_engine.bus";
    "from core\.logger" = "from utils.logger";
    "from core\.demo_simulator" = "from backend.event_engine.demo_simulator";
    "from core\.event_simulator" = "from backend.event_engine.event_simulator";
    "from security\." = "from backend.threat_engine.";
    "import security\." = "import backend.threat_engine.";
    "from ai\.copilot" = "from backend.copilot.copilot";
    "import ai\.copilot" = "import backend.copilot.copilot";
    "from ai\.agentic\." = "from backend.agents.agentic.";
    "import ai\.agentic\." = "import backend.agents.agentic.";
    "from evaluation\.analytics_dashboard" = "from pages.4_AI_Analytics";
    "from evaluation\." = "from backend.agents.evaluation.";
    "import evaluation\." = "import backend.agents.evaluation.";
    "from ai\." = "from backend.ai_brain.";
    "import ai\." = "import backend.ai_brain.";
    "from simulation\." = "from backend.simulation.";
    "import simulation\." = "import backend.simulation.";
    "from ui\.theme" = "from frontend.theme";
    "from ui\.layout" = "from frontend.layout";
    "from ui\.components" = "from frontend.components";
    "from ui\.charts" = "from frontend.charts";
}

Get-ChildItem -Path $root -Recurse -Filter *.py | ForEach-Object {
    $content = Get-Content $_.FullName -Raw
    $changed = $false
    foreach ($key in $replacements.Keys) {
        if ($content -match $key) {
            $content = [regex]::Replace($content, $key, $replacements[$key])
            $changed = $true
        }
    }
    if ($changed) {
        Set-Content -Path $_.FullName -Value $content -NoNewline
    }
}
Write-Host "Refactoring complete."
