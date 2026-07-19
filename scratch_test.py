import sys
import os

# mock streamlit secrets logic
import streamlit as st
st.secrets = {}

from backend.copilot.copilot import StadiumCopilot

try:
    copilot = StadiumCopilot()
    response = copilot.ask("What is the risk of a crush at Gate A?")
    print("SUCCESS!")
    print(response)
except Exception as e:
    import traceback
    traceback.print_exc()
