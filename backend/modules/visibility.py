import numpy as np

def is_visible(sat_eci_km, observer_eci_km):
    if (observer_eci_km == None): return "OBSERVER NOT DEFINED"
    # Convert to NumPy arrays
    sat = np.array(sat_eci_km)
    obs = np.array(observer_eci_km)

    # Vector from observer to satellite
    sat_rel = sat - obs

    # Normalize observer vector to get local zenith direction
    zenith = obs / np.linalg.norm(obs)

    # Elevation angle is the angle between sat_rel and zenith
    cos_angle = np.dot(sat_rel, zenith) / np.linalg.norm(sat_rel)
    elevation_rad = np.arcsin(cos_angle)

    # Satellite is visible if elevation > 0
    if elevation_rad > 0: return "TRUE"
    else: return "FALSE"