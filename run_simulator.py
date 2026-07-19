from simulator.engine import SimulatorEngine
from backend.event_engine.store import event_store
from backend.stadium_state.stadium_state import stadium_state_aggregator
import simulator.correlation  # To initialize the engine
from utils.logger import logger
from backend.event_engine.event_bus import event_bus, Subscriber
from backend.event_engine.models import StadiumEvent
import json

class ConsolePreviewer(Subscriber):
    def update(self, event: StadiumEvent) -> None:
        """A simple subscriber just for stdout printing to show it works."""
        if event.severity.value in ["WARNING", "CRITICAL"]:
            print(f"[{event.timestamp.strftime('%H:%M:%S')}] [{event.category.value}] [{event.severity.value}] {event.location} - {event.description}")

previewer = ConsolePreviewer()

def main():
    logger.info("Booting StadiumOS Backend Foundation (Phase 1)...")
    
    # Subscribe our console previewer
    event_bus.subscribe(previewer, topic=None)
    
    # Initialize engines
    engine = SimulatorEngine()
    from simulator.scenario_engine import scenario_engine, ScenarioStage, Branch
    
    # Load a sample Kickoff scenario
    kickoff_stages = {
        "Crowd Surge": ScenarioStage(
            name="Crowd Surge",
            delay_secs=5,
            events_to_generate=[{
                "category": "CROWD",
                "severity": "WARNING",
                "priority": "HIGH",
                "source": "ScenarioEngine",
                "location": "Gate A",
                "metrics": {"surge": True},
                "description": "Massive crowd surge ahead of kickoff."
            }],
            branches=[Branch(next_stage="Gate Delay", probability=1.0)]
        ),
        "Gate Delay": ScenarioStage(
            name="Gate Delay",
            delay_secs=5,
            events_to_generate=[{
                "category": "GATE",
                "severity": "CRITICAL",
                "priority": "HIGH",
                "source": "ScenarioEngine",
                "location": "Gate A",
                "metrics": {"wait_time": 60},
                "description": "Gate A overloaded. 60+ min wait."
            }],
            branches=[Branch(next_stage="Recovery", probability=1.0)]
        ),
        "Recovery": ScenarioStage(
            name="Recovery",
            delay_secs=0,
            events_to_generate=[{
                "category": "GATE",
                "severity": "INFO",
                "priority": "LOW",
                "source": "ScenarioEngine",
                "location": "Gate A",
                "metrics": {"wait_time": 5},
                "description": "Gate A recovered. Crowd dispersed."
            }]
        )
    }
    
    scenario_engine.start_scenario("Kickoff Chaos", kickoff_stages, "Crowd Surge")
    
    print("\n--- STADIUM OS PHASE 1 SIMULATOR ---")
    print("Generating stateful events. Event Store & State are syncing in the background.")
    print("Printing WARNING and CRITICAL events to console...\n")
    
    try:
        engine.run_forever()
    except KeyboardInterrupt:
        pass
        
    print("\n--- SHUTTING DOWN ---")
    
    # Verify the Event Store and State
    print(f"Event Store contains {len(event_store._buffer)} events.")
    
    print("\nOperational Summary from StadiumStateAggregator:")
    print(stadium_state_aggregator.get_operational_summary())
    
    print("\nGlobal Snapshot (Flattened):")
    print(json.dumps(stadium_state_aggregator.get_dashboard_snapshot(), indent=2, default=str))

if __name__ == "__main__":
    main()
