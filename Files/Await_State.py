from Drone_State import DroneState

class AwaitState(DroneState):
    def __init__(self, taken_energy=0):
        super().__init__(taken_energy)

    def take_energy(self):
        return self.taken_energy_amount
        
    def act(self, drone):
        pass