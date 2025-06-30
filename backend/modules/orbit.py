from sgp4.api import Satrec
from sgp4.conveniences import jday_datetime
from datetime import datetime
import numpy as np
import pymap3d as pm

def eci_to_geodetic(position_eci_km, dt):
    x, y, z = position_eci_km
    # ECI to ECEF (requires time in UTC)
    x_ecef, y_ecef, z_ecef = pm.eci2ecef(x * 1000, y * 1000, z * 1000, dt)  # Convert to meters
    # ECEF to geodetic
    lat, lon, alt = pm.ecef2geodetic(x_ecef, y_ecef, z_ecef)
    return (lat, lon, alt / 1000)  # Return altitude in kilometers

def propagate(dt: datetime, tle1: str, tle2: str):
    satellite = Satrec.twoline2rv(tle1, tle2)
    jd, fr = jday_datetime(dt)
    e, r, v = satellite.sgp4(jd, fr)
    if e != 0:
        raise RuntimeError(f"SGP4 error: {e}")
    pos_eci = r # km
    pos_geo = eci_to_geodetic(pos_eci, dt)
    vel_eci = v # km/s
    vel = np.linalg.norm(v)
    return pos_eci, pos_geo, vel_eci, vel



