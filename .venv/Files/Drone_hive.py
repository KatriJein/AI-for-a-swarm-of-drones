from Drone import Drone
from Await_State import AwaitState

class DroneHive:
    def __init__(self, map):
        self.__map = map
        self.__drones = []
        self.__postponed_orders = []
    
    def add_drone(self, drone):
        if isinstance(drone, Drone):
            self.__drones.append(drone)
    
    def act(self):
        for drone in self.__drones:
            drone.act()

    def draw(self):
        for drone in self.__drones:
            drone.draw()

    def set_order(self, order):
        candidates = []
        for drone in self.__drones:
            if isinstance(drone.get_state(), AwaitState):
                data = drone.can_take_order(self.__map, order)
                if data[0]:
                    candidates.append((drone, data[1]))
        if not candidates:
            self.__postponed_orders.append(order)
            return
        best_candidate = min(candidates, key=lambda t: (t[1], t[0].get_id()))[0]
        best_candidate.take_order(self.__map, order)