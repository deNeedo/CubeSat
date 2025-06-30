import time
from datetime import datetime, timezone, timedelta

class SimulationClock:
    def __init__(self, speed=1.0):
        self.speed = speed
        self.real_time_ref = datetime.now(timezone.utc)
        self.sim_time_ref = self.real_time_ref

    def set_speed(self, new_speed):
        # Update sim_time_ref to preserve continuity
        now = datetime.now(timezone.utc)
        elapsed_real = (now - self.real_time_ref).total_seconds()
        self.sim_time_ref += timedelta(seconds=elapsed_real * self.speed)
        
        self.real_time_ref = now
        self.speed = new_speed

    def reset(self):
        self.real_time_ref = datetime.now(timezone.utc)
        self.sim_time_ref = self.real_time_ref
        self.speed = 1.0

    def now(self):
        elapsed_real = (datetime.now(timezone.utc) - self.real_time_ref).total_seconds()
        return self.sim_time_ref + timedelta(seconds=elapsed_real * self.speed)
