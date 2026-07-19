import json
import time
import random
from datetime import datetime

class StadiumEventSimulator:
    """
    Live Event Simulator for StadiumOS.
    Generates fake live feeds as JSON events for:
    - Crowd
    - Ticket
    - Weather
    - IoT
    - Network
    - Gate
    - Medical
    """
    def __init__(self):
        self.gates = ['Gate A', 'Gate B', 'Gate C', 'Gate D', 'VIP Entrance']
        self.weather_conditions = ['Clear', 'Cloudy', 'Light Rain', 'Heavy Rain', 'Thunderstorm']
        self.network_status = ['Normal', 'Degraded', 'Offline', 'High Latency']
        self.ticket_events = ['Valid Scan', 'Invalid Scan', 'Duplicate Scan', 'VIP Entry']
        self.medical_events = ['Normal', 'Minor Injury', 'Fan Fainted', 'Dehydration']

    def generate_crowd_event(self):
        return {
            "type": "Crowd",
            "location": random.choice(self.gates + ["Zone 1", "Zone 2", "Food Court"]),
            "occupancy_percent": random.randint(40, 100),
            "movement_speed": round(random.uniform(0.5, 2.5), 2),
            "timestamp": datetime.now().isoformat()
        }

    def generate_ticket_event(self):
        # Weight towards valid scans, but simulate some errors
        status = random.choices(self.ticket_events, weights=[0.8, 0.05, 0.05, 0.1])[0]
        return {
            "type": "Ticket",
            "gate": random.choice(self.gates),
            "status": status,
            "timestamp": datetime.now().isoformat()
        }

    def generate_weather_event(self):
        return {
            "type": "Weather",
            "condition": random.choice(self.weather_conditions),
            "temperature_c": round(random.uniform(15.0, 35.0), 1),
            "timestamp": datetime.now().isoformat()
        }

    def generate_iot_event(self):
        return {
            "type": "IoT",
            "sensor": f"Sensor_{random.randint(1, 100)}",
            "power_status": random.choices(["Online", "Warning", "Offline"], weights=[0.9, 0.05, 0.05])[0],
            "temperature_c": round(random.uniform(20.0, 30.0), 1),
            "timestamp": datetime.now().isoformat()
        }

    def generate_network_event(self):
        return {
            "type": "Network",
            "zone": random.choice(["North Stand", "South Stand", "East Stand", "West Stand"]),
            "status": random.choices(self.network_status, weights=[0.85, 0.05, 0.05, 0.05])[0],
            "timestamp": datetime.now().isoformat()
        }

    def generate_gate_event(self):
        return {
            "type": "Gate",
            "gate": random.choice(self.gates),
            "wait_time_minutes": random.randint(1, 45),
            "throughput_per_minute": random.randint(10, 50),
            "timestamp": datetime.now().isoformat()
        }

    def generate_medical_event(self):
        return {
            "type": "Medical",
            "location": random.choice(["Sector 1", "Sector 2", "Sector 3", "VIP Lounge"]),
            "status": random.choices(self.medical_events, weights=[0.9, 0.05, 0.02, 0.03])[0],
            "timestamp": datetime.now().isoformat()
        }

    def generate_random_event(self):
        event_generators = [
            self.generate_crowd_event,
            self.generate_ticket_event,
            self.generate_weather_event,
            self.generate_iot_event,
            self.generate_network_event,
            self.generate_gate_event,
            self.generate_medical_event
        ]
        
        generator = random.choice(event_generators)
        return generator()

    def run(self, interval_seconds=1.0):
        print("Starting StadiumOS Live Event Simulator...")
        print("Generating real-time JSON events for Stadium operations...\n")
        try:
            while True:
                event = self.generate_random_event()
                print(json.dumps(event))
                time.sleep(interval_seconds)
        except KeyboardInterrupt:
            print("\nSimulator stopped.")

if __name__ == "__main__":
    simulator = StadiumEventSimulator()
    # Adjust interval to control the frequency of events
    simulator.run(interval_seconds=2.0)
