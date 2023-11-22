
from .Drone_State import DroneState

class FlyingState(DroneState):
    def __init__(self, target, taken_energy=0.4):
        super().__init__(taken_energy)
        self.__target = target

    def act(self, drone):
        location = drone.get_location()
        location.x += self.__target.x
        location.y += self.__target.y