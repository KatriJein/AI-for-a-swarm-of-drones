from Shared_constants import FLY_POINTS_IN_SECOND

class DroneState:
    def __init__(self, taken_energy):
        self.taken_energy_amount = taken_energy / FLY_POINTS_IN_SECOND

    def take_energy(self):
        return self.taken_energy_amount
    
    def act(self, drone):
        pass