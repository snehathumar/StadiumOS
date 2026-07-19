import os
import sys
# Mock streamlit secrets
import streamlit as st
st.secrets = {}

from backend.event_engine.demo_simulator import demo_simulator

print("Testing Scenario 1...")
demo_simulator.inject_scenario_1_overcrowding()
print("Scenario 1 Success!")

print("Testing Scenario 2...")
demo_simulator.inject_scenario_2_security_threat()
print("Scenario 2 Success!")

print("Testing Scenario 3...")
demo_simulator.inject_scenario_3_predictive_simulation()
print("Scenario 3 Success!")
