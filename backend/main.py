from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from threading import Thread
from time import sleep
from time_controller import SimulationClock
from state import SimulationState
from modules import orbit, sun, shadow, magnetic_field
import requests

# Global simulation state
clock = SimulationClock(speed=1.0)
state = SimulationState()

# Simulation loop
def simulation_loop():
    while True:
        state.datetime = clock.now()
        state.position_eci, state.position_geo, state.velocity_eci = orbit.propagate(state.datetime, line1, line2)
        state.sun_vector = sun.compute_vector(state.datetime)
        state.in_shadow = shadow.is_in_umbra(state.position_eci, state.sun_vector)
        state.magnetic_field = magnetic_field.compute(state.position_eci, state.datetime)
        sleep(0.1)

url = "https://celestrak.org/NORAD/elements/gp.php?CATNR=25544&FORMAT=tle"
response = requests.get(url)

if response.status_code == 200:
    tle_lines = response.text.strip().split('\n')
    # Usually TLE has 3 lines: name, line1, line2
    state.name = tle_lines[0]
    line1 = tle_lines[1]
    line2 = tle_lines[2]
    # Start simulation in a background thread
    Thread(target=simulation_loop, daemon=True).start()
else:
    print(f"Failed to fetch TLE data. Status code: {response.status_code}")

app = FastAPI()

# Enable CORS so frontend can access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # adjust if needed
    allow_methods=["*"],
    allow_headers=["*"],
)

# API route to expose orbit data
@app.get("/state")
def get_state():
    return {
        "name": state.name,
        "position_eci": state.position_eci,
        "position_geo": state.position_geo,
    }

    # "datetime": state.datetime.isoformat(),
    # "position_eci": state.position_eci,
    # "velocity_eci": state.velocity_eci,
    # "sun_vector": state.sun_vector,
    # "in_shadow": state.in_shadow,
    # "magnetic_field": state.magnetic_field
