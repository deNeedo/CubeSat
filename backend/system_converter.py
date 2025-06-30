import pymap3d as pm
from datetime import datetime, timezone

# def geodetic_to_ecef():

def geodetic_to_eci(lat, lon, alt_km):
    dt = datetime.now(timezone.utc)
    x, y, z = pm.geodetic2eci(lat, lon, alt_km * 1000, dt)  # meters
    return (x / 1000, y / 1000, z / 1000)  # Return in kilometers

def eci_to_geodetic(position_eci_km, dt):
    x, y, z = position_eci_km
    # ECI to ECEF (requires time in UTC)
    x_ecef, y_ecef, z_ecef = pm.eci2ecef(x * 1000, y * 1000, z * 1000, dt)  # Convert to meters
    # ECEF to geodetic
    lat, lon, alt = pm.ecef2geodetic(x_ecef, y_ecef, z_ecef)
    return (lat, lon, alt / 1000)  # Return altitude in kilometers