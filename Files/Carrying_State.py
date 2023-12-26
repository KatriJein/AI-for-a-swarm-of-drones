
from Drone_State import DroneState
from Await_State import AwaitState

class CarryingState(DroneState):
    def __init__(self, shipment, taken_energy=0.4, carry_together=False):
        super().__init__(taken_energy)
        self.__shipment = shipment
        self.__target = shipment
        self.__carrying_together = carry_together
        # self.__target = target

    def take_energy(self):
        return (super().take_energy() * self.__shipment.weight / 1000) / (1 if not self.__carrying_together else 2)
    
    def act(self, drone):
        step = drone.next_move()
        if step is None and drone.get_location().get_position() == self.__target.dest_pos.get_position():
            self.__target.delivered_by_drone()
            drone.get_hive().delivered_orders.add(self.__target)
            drone.del_order_id()
            drone.set_partner(None)
            drone.wait()
            #drone.set_state(AwaitState())
            #drone.set_order_id(None)
            return
        # if step is None:
        #     # drone.wait()
        #     # print(drone.get_state())
        #     return
        drone_loc = drone.get_location()
        drone_loc.x = step.x
        drone_loc.y = step.y
        drone.take_energy()