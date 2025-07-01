from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from threading import Thread
from time import sleep
from time_controller import SimulationClock
from state import SimulationState
from modules import orbit, sun, shadow, magnetic_field, visibility
from pydantic import BaseModel
from system_converter import geodetic_to_eci, gmst_angle
import requests

# Global simulation state
clock = SimulationClock(speed=1.0)
state = SimulationState()

# Simulation loop
def simulation_loop():
    while True:
        state.datetime = clock.now()
        state.position_eci, state.position_geo, state.velocity_eci, state.velocity = orbit.propagate(state.datetime, line1, line2)
        state.sun_vector = sun.compute_vector(state.datetime)
        state.in_shadow = shadow.is_in_umbra(state.position_eci, state.sun_vector)
        state.magnetic_field = magnetic_field.compute(state.position_eci, state.datetime)
        state.is_visible = visibility.is_visible(state.position_eci, state.observer_eci)
        sleep(0.1)

url = "https://celestrak.org/NORAD/elements/gp.php?CATNR=25544&FORMAT=tle"
# response = requests.get(url)

# if response.status_code == 200:
#     tle_lines = response.text.strip().split('\n')
#     # Usually TLE has 3 lines: name, line1, line2
#     state.name = tle_lines[0]
#     line1 = tle_lines[1]
#     line2 = tle_lines[2]
#     # Start simulation in a background thread
#     Thread(target=simulation_loop, daemon=True).start()
# else:
#     print(f"Failed to fetch TLE data. Status code: {response.status_code}")

state.name = "ISS (ZARYA)"
line1 = "1 25544U 98067A   25181.86034722  .00005730  00000+0  10713-3 0  9998"
line2 = "2 25544  51.6365 239.3035 0002095 317.1043  16.2145 15.50312841517279"

Thread(target=simulation_loop, daemon=True).start()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://192.168.0.103:3000",
        "http://10.147.17.201:3000", # your actual frontend IP + port
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SpeedRequest(BaseModel):
    speed: float

@app.get("/rotangle")
def get_state():
    return gmst_angle()

@app.get("/observer-eci")
def get_observer_eci(lat: float = Query(...), lon: float = Query(...)):
    state.observer_eci = geodetic_to_eci(lat, lon, 0.0)
    return state.observer_eci

@app.post("/reset")
def reset():
    clock.reset()

@app.post("/speed")
def set_speed(req: SpeedRequest):
    clock.set_speed(req.speed)

# API route to expose orbit data
@app.get("/state")
def get_state():
    return {
        "name": state.name,
        "datetime": state.datetime,
        "position_eci": state.position_eci,
        "position_geo": state.position_geo,
        "velocity_eci": state.velocity_eci,
        "velocity": state.velocity,
        "sun_eci": state.sun_vector,
        "magnetic_field": state.magnetic_field,
        "in_shadow": state.in_shadow,
        "visible": state.is_visible,
        # "sun_vector": state.sun_vector,
        # "earth_vector": state.earth_vector,
        # "magnetic_field": state.magnetic_field,
        
        # "face_powers": state.face_powers,
        # "attitude_matrix" = state.attitude_matrix
    }
