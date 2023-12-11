from Drone import Drone
from Await_State import AwaitState
from Flying_State import FlyingState
from Carrying_State import CarryingState

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

    def send_order_request(self, drone, order_data):
        order = order_data[0]
        best_candidate = (drone, order_data[1])
        for d in self.__drones:
            if d.get_id() != drone.get_id() and isinstance(d.get_state(), AwaitState):
                data = d.can_take_order(order)
                if data[0]:
                    distance_to_order = data[1]
                    if distance_to_order < best_candidate[1]:
                        best_candidate = (d, distance_to_order)
        self.orders.remove(order)
        best_candidate[0].set_order_id(order.get_id())
        best_candidate[0].fly(order)

    #def choose_drone(self, order):
        #best_candidate = None 
        #min_dist = float('inf')

        #for drone in self.__drones:
            #if drone.can_take_order(self.map, order.location.get_position()) and isinstance(drone.get_state(), AwaitState):
                #dist = drone.path_distance()
                #if dist < min_dist:
                    #best_candidate = drone 
                    #min_dist = dist 
        #return best_candidate

    def set_order(self, order):
         self.orders.append(order)
        #for order in self.orders:
            #best_candidate = self.choose_drone(order)
            #best_candidate.set_state(FlyingState(order))
            #self.orders.remove(order)
         for drone in self.__drones:
             drone.take_order()