class SimulationState:
    def __init__(self):
        self.datetime = None
        self.name = None
        self.observer_eci = None
        self.position_eci = None
        self.position_geo = None
        self.velocity_eci = None
        self.velocity = None
        self.in_shadow = False
        self.sun_vector = None
        self.magnetic_field = None
        self.is_visible = False
        self.face_powers = None
        self.attitude_matrix = None
        
