# To install Streamlit, run the following command in your terminal:
# pip install streamlit

import random

# Initial specification setup
def simulation_specification():
    return {
        "vessel_min_moves": 500,
        "vessel_max_moves": 3000,
        "default_moves": 1500,
        "min_cranes": 1,
        "max_cranes": 4,
        "default_cranes": 2,
        "min_mph": 20,
        "max_mph": 40,
        "default_min_mph": 25,
        "default_max_mph": 30,
        "day_hours": 24
    }

specs = simulation_specification()

# Mock Streamlit for environments without streamlit support
class MockStreamlit:
    def set_page_config(self, **kwargs):
        pass
    def title(self, text):
        print(f"# {text}")
    def slider(self, label, min_value, max_value, value=None, step=1):
        print(f"{label} ({min_value}-{max_value}, default={value}):")
        return value if value is not None else min_value
    def subheader(self, text):
        print(f"\n## {text}")
    def write(self, text):
        print(text)
    def progress(self, value, text=""):
        percent = int(value * 100)
        print(f"[{percent}%] {text}")

try:
    import streamlit as st
except ModuleNotFoundError:
    print("Warning: Streamlit not found. Using mock version.")
    st = MockStreamlit()

st.set_page_config(page_title="Port Terminal Digital Twin", layout="wide")

st.title("🚢 Port Terminal Simulation")

# Parameters
vessel_moves = st.slider("Total container moves required for vessel", specs["vessel_min_moves"], specs["vessel_max_moves"], specs["default_moves"], step=100)
cranes_assigned = st.slider("Number of cranes assigned", specs["min_cranes"], specs["max_cranes"], specs["default_cranes"])

# Crane productivity range
min_mph = st.slider("Minimum crane moves/hour", specs["min_mph"], specs["default_max_mph"], specs["default_min_mph"])
max_mph = st.slider("Maximum crane moves/hour", specs["default_min_mph"], specs["max_mph"], specs["default_max_mph"])

# Simulate crane performance
crane_mph = [random.randint(min_mph, max_mph) for _ in range(cranes_assigned)]
total_mph = sum(crane_mph)

# Calculate vessel port stay
time_required = vessel_moves / total_mph

# Output results
st.subheader("📊 Simulation Results")
st.write(f"**Crane performance (moves/hour):** {crane_mph}")
st.write(f"**Total productivity:** {total_mph} moves/hour")
st.write(f"**Estimated time in port:** {time_required:.2f} hours")

# Visual
st.progress(min(time_required / specs["day_hours"], 1.0), text="Vessel processing progress")
