
# To install Streamlit, run:
# pip install streamlit

import streamlit as st
import random
import json
import matplotlib.pyplot as plt

# Load specs
with open("specs.json", "r") as f:
    specs = json.load(f)

st.set_page_config(page_title="Port Terminal Digital Twin", layout="wide")
st.title("🚢 Port Terminal Simulation")

# User input for number of vessels
num_vessels = st.slider("Number of vessels to simulate", 1, 10, specs["number_of_vessels"])

results = []

for vessel_idx in range(num_vessels):
    st.subheader(f"Vessel {vessel_idx+1}")
    vessel_moves = st.slider(f"Vessel {vessel_idx+1} - Total container moves", specs["vessel_min_moves"], specs["vessel_max_moves"], specs["default_moves"], step=100)
    cranes_assigned = st.slider(f"Vessel {vessel_idx+1} - Cranes assigned", specs["min_cranes"], specs["max_cranes"], specs["default_cranes"])
    min_mph = st.slider(f"Vessel {vessel_idx+1} - Min crane moves/hour", specs["min_mph"], specs["default_max_mph"], specs["default_min_mph"])
    max_mph = st.slider(f"Vessel {vessel_idx+1} - Max crane moves/hour", specs["default_min_mph"], specs["max_mph"], specs["default_max_mph"])

    crane_mph = [random.randint(min_mph, max_mph) for _ in range(cranes_assigned)]
    total_mph = sum(crane_mph)
    time_required = vessel_moves / total_mph

    st.write(f"**Crane performance (moves/hour):** {crane_mph}")
    st.write(f"**Total productivity:** {total_mph} moves/hour")
    st.write(f"**Estimated time in port:** {time_required:.2f} hours")
    st.progress(min(time_required / specs["day_hours"], 1.0), text="Vessel processing progress")

    results.append((vessel_idx+1, crane_mph, total_mph, time_required))

# Productivity Visualization
st.subheader("📈 Productivity Visualization")
for vessel_id, crane_mph, total_mph, _ in results:
    fig, ax = plt.subplots()
    ax.bar(range(1, len(crane_mph)+1), crane_mph)
    ax.set_title(f"Vessel {vessel_id} - Crane Productivity")
    ax.set_xlabel("Crane Number")
    ax.set_ylabel("Moves per Hour")
    st.pyplot(fig)
