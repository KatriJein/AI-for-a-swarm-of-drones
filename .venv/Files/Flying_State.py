
from Drone_State import DroneState

class FlyingState(DroneState):
    def __init__(self, target, taken_energy=0.4):
        super().__init__(taken_energy)
        self.__target = target

    def act(self, drone):
        step = drone.next_move()
        if step is None:
            drone.wait()
            return
        drone_loc = drone.get_location()
        drone_loc.x = step.x
        drone_loc.y = step.y
        drone.take_energy()