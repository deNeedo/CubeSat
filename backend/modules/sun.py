import numpy as np
from datetime import datetime
from sgp4.conveniences import jday_datetime

def compute_vector(dt: datetime):
    # Julian centuries since J2000.0
    jd, fr = jday_datetime(dt)
    T = (jd - 2451545.0) / 36525.0

    # Mean longitude (deg)
    L = (280.460 + 36000.770 * T) % 360
    # Mean anomaly (deg)
    M = (357.528 + 35999.050 * T) % 360

    # Ecliptic longitude (deg)
    lambda_sun = L + 1.915 * np.sin(np.radians(M)) + 0.020 * np.sin(np.radians(2 * M))
    lambda_rad = np.radians(lambda_sun)

    # Distance to Sun in AU
    r = 1.00014 - 0.01671 * np.cos(np.radians(M)) - 0.00014 * np.cos(np.radians(2 * M))
    r_km = r * 149597870.7  # AU → km

    # Convert to ECI assuming Earth's obliquity
    epsilon = np.radians(23.439281)
    x = r_km * np.cos(lambda_rad)
    y = r_km * np.cos(epsilon) * np.sin(lambda_rad)
    z = r_km * np.sin(epsilon) * np.sin(lambda_rad)
    return (x, y, z) # km
