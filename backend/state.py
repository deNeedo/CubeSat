class SimulationState:
    def __init__(self):
        self.name = None
        self.datetime = None
        self.position_eci = None
        self.position_geo = None
        self.velocity_eci = None
        self.attitude_matrix = None
        self.sun_vector = None
        self.magnetic_field = None
        self.face_powers = None
        self.in_shadow = False
