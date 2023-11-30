from Drone import Drone
from Await_State import AwaitState

class DroneHive:
    def __init__(self, map_):
        self.__drones = []
        self.orders = []
        self.map = map_
    
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
        self.orders.append(order)
        for drone in self.__drones:
            drone.take_order(self.map)