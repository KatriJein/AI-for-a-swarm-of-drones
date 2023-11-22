
from .Drone_State import DroneState

class CarryingState(DroneState):
    def __init__(self, shipment, target, taken_energy=0.4):
        super().__init__(taken_energy)
        self.__shipment = shipment
        self.__target = target

    def take_energy(self):
        return super().take_energy() * self.__shipment.weight
    
    def act(self, drone):
        pass