from system_converter import eci_to_geodetic
import numpy as np
from geomag import geomag

gm = geomag.GeoMag()

def compute(sat_pos_eci: np.ndarray, dt):
    lat, lon, alt_km = eci_to_geodetic(sat_pos_eci, dt)
    result = gm.GeoMag(lat, lon, alt_km, time=dt.date())
    mag = np.linalg.norm((result.bx, result.by, result.bz))
    return mag
