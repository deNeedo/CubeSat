from pymap3d import eci2ecef, ecef2geodetic, geodetic2eci, geodetic2ecef
from numpy import floor
from sgp4.conveniences import jday_datetime
from datetime import datetime, timezone

def geodetic_to_eci(lat, lon, alt_km):
    dt = datetime.now(timezone.utc)
    x, y, z = geodetic2eci(lat, lon, alt_km * 1000, dt)  # meters
    return (x / 1000, y / 1000, z / 1000)  # Return in kilometers

def eci_to_geodetic(position_eci_km, dt):
    x, y, z = position_eci_km
    # ECI to ECEF (requires time in UTC)
    x_ecef, y_ecef, z_ecef = eci2ecef(x * 1000, y * 1000, z * 1000, dt)  # Convert to meters
    # ECEF to geodetic
    lat, lon, alt = ecef2geodetic(x_ecef, y_ecef, z_ecef)
    return (lat, lon, alt / 1000)  # Return altitude in kilometers

from datetime import datetime
from math import pi

def gmst_angle() -> float:
    dt = datetime.now(timezone.utc)
    jd, fr = jday_datetime(dt)

    # # Julian date
    # Y, M = dt.year, dt.month
    # D = dt.day + (dt.hour + dt.minute / 60 + dt.second / 3600) / 24
    # if M <= 2:
    #     Y -= 1
    #     M += 12
    # A = floor(Y / 100)
    # B = 2 - A + floor(A / 4)
    # JD = floor(365.25 * (Y + 4716)) + floor(30.6001 * (M + 1)) + D + B - 1524.5

    JD = jd + fr
    # Julian days since J2000.0
    T = JD - 2451545.0
    ERA = 2 * pi * (0.7790572732640 + 1.00273781191135448 * T) - pi/2
    ERA = ERA % (2*pi)

    # # GMST in seconds
    # GMST_sec = 67310.54841 + (876600 * 3600 + 8640184.812866) * T \
    #            + 0.093104 * T**2 - 6.2e-6 * T**3

    # # Convert to radians
    # GMST_deg = (GMST_sec / 240.0) % 360.0
    # GMST_rad = GMST_deg * pi / 180.0
    return ERA
