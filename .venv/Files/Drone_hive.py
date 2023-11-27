from Drone import Drone

class DroneHive:
    def __init__(self):
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
            if drone.view_order(order):
                candidates.append(drone)
        if not candidates:
            self.__postponed_orders.append(order)
            return
        best_candidate = min(candidates, key=lambda d: d.get_id())
        best_candidate.take_order(order)