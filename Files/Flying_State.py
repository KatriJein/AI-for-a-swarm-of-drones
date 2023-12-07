from Carrying_State import CarryingState
from Charging_State import ChargingState
from Drone_State import DroneState
from order_obstacles import Order
from Location import Location

class FlyingState(DroneState):
    def __init__(self, target, taken_energy=0.4):
        super().__init__(taken_energy)
        self.__target = target

    def act(self, drone):
        step = drone.next_move()
        if step is None:
            if isinstance(self.__target, Order):
                pos = self.__target.location.get_position()
                if (drone.get_location().get_position() == pos):
                    self.__target.taken_by_drone()
                    drone.set_order_id(self.__target.get_id())
                    drone.build_path(self.__target.dest_pos)
                    drone.carry_to(self.__target)
                    return
            elif isinstance(self.__target, Location):
                pos = self.__target.get_position()
                if (drone.get_location().get_position() == pos):
                    drone.set_state(ChargingState())
                    return

            
        if step is None:
            drone.wait()
            return
        drone_loc = drone.get_location()
        drone_loc.x = step.x
        drone_loc.y = step.y
        drone.take_energy()