import numpy as np

EARTH_RADIUS_KM = 6371.0

def is_in_umbra(sat_pos_eci: np.ndarray, sun_vector_eci: np.ndarray) -> bool:
    sat_vec = sat_pos_eci
    sun_vec = sun_vector_eci

    sun_unit = sun_vec / np.linalg.norm(sun_vec)
    sat_proj = np.dot(sat_vec, sun_unit)
    proj_point = sun_unit * sat_proj

    orth_vec = sat_vec - proj_point
    distance_from_axis = np.linalg.norm(orth_vec)

    # Umbra condition: satellite is behind Earth and inside shadow cylinder
    if sat_proj < 0 and distance_from_axis < EARTH_RADIUS_KM:
        return True
    return False
