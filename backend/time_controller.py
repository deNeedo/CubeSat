import time
from datetime import datetime, timezone, timedelta

class SimulationClock:
    def __init__(self, start_time=None, speed=1.0):
        self.sim_start = start_time or datetime.now(timezone.utc)
        self.speed = speed
        self.wall_start = time.time()

    def now(self):
        elapsed_wall = time.time() - self.wall_start
        sim_elapsed = elapsed_wall * self.speed
        return self.sim_start + timedelta(seconds=sim_elapsed)
