import turtle, os

from queue import Queue

from Drone_Constants import ID_GENERATOR, COLOR_GENERATOR, BATTERY_CHARGE, FLIGHT_ALTITUDE, DRONE_WIDTH, DRONE_LENGTH
from Shared_constants import FLY_POINTS_IN_SECOND, VERY_LOW_CHARGE, HEAVY_ORDER_SIDE
from Location import Location
from Battery import Battery
from Station import Station
from order_obstacles import Barrier
from Await_State import AwaitState
from Flying_State import FlyingState
from Carrying_State import CarryingState
from Charging_State import ChargingState
from Wait_For_Help_State import WaitForHelpState

try:
    drone_path = os.path.join("_internal", "Images", "drone.gif")
    turtle.register_shape(drone_path)
except:
    drone_path = os.path.join("Files", "Images", "drone.gif")
    turtle.register_shape(drone_path)

class Drone:
    def __init__(self, hive, station, width=DRONE_WIDTH, length=DRONE_LENGTH):
        self.__id = ID_GENERATOR.get_id()
        self.__width = width
        self.__length = length
        self.__location = Location(580, 400, z=FLIGHT_ALTITUDE)
        self.__battery = Battery(charge=BATTERY_CHARGE)
        self.__state = AwaitState()
        self.__flight_altitude = self.__location.z
        self.__order_id = None
        self.__station = station
        self.__path = []
        self.__hive = hive
        self.__partner = None

        self.__set_graphics()

    def __set_graphics(self):
        global drone_path
        self.__turtle = turtle.Turtle(shape=drone_path)
        self.__text_turtle = turtle.Turtle()
        self.__text_turtle.hideturtle()
        self.__text_turtle.speed("fastest")
        self.__text_turtle.color("black")
        self.__turtle.shapesize(self.__width, self.__length, 1)
        self.__turtle.pensize(3)
        self.__turtle.speed(2)
        self.__turtle.up()
        self.__turtle.setposition(self.__location.get_position())
        self.__turtle.color(*COLOR_GENERATOR.get_inactive_state_color())
        self.__active_color = COLOR_GENERATOR.generate_color()

    def draw(self):
        self.__text_turtle.clear()
        loc = self.__location.get_position()
        self.__turtle.goto(loc)
        text_pos = (loc[0] - 70, loc[1] + 10)
        self.__text_turtle.goto(text_pos)
        self.__text_turtle.write(f"Id: {self.__id}, заряд: {round(self.__battery.get_charge(), 2)}", font=("Times New Roman", 15, "bold"))
        

    def act(self):
        self.__state.act(self)

    def take_energy(self):
        self.__battery.take_energy(self.__state.take_energy())

    def path_distance(self, optional_path=None):
        path = self.__path if optional_path is None else optional_path
        completed_steps = 0
        for i in range(1, len(path)):
            cur_loc = path[i].get_position()
            prev_loc = path[i - 1].get_position()
            completed_steps += abs(cur_loc[0] - prev_loc[0]) + abs(cur_loc[1] - prev_loc[1])
        return completed_steps
            
    def calculate_battery_spending(self, *args):
        taken_energy = 0
        for arg in args:
            steps = 0
            path, condition = None, None
            if isinstance(arg, tuple):
                path, condition = arg
            else:
                path = arg
            steps += self.path_distance(path)
            taken_energy += (self.__state if condition is None else condition).take_energy() * (steps / FLY_POINTS_IN_SECOND)
        return taken_energy
    
    def __get_track(self, cur_pos, start, end, map_):
        track = {}
        track[start] = None
        queue = Queue()
        queue.put((start, cur_pos))
        while queue.qsize() != 0:
            pos = queue.get()
            neighbours = ((pos[1][0] - 1, pos[1][1]), (pos[1][0] + 1, pos[1][1]), (pos[1][0], pos[1][1] + 1), (pos[1][0], pos[1][1] - 1))
            for n_pos in neighbours:
                if n_pos[0] >= 0 and n_pos[0] <= len(map_.map) - 1 and n_pos[1] >= 0 and n_pos[1] <= len(map_.map[0]) - 1:
                    next_elem = map_.map[n_pos[0]][n_pos[1]]
                    if (next_elem in track or (self.__order_id is not None and self.__flight_altitude <= next_elem.z and isinstance(next_elem.obj_at_location, (Barrier, Station)))
                        or (self.__order_id is None and self.__flight_altitude <= next_elem.z and isinstance(next_elem.obj_at_location, Barrier))):
                        continue
                    track[next_elem] = pos[0]
                    queue.put((next_elem, n_pos))
            if end in track:
                break
        
        return track


    def build_path(self, target, from_=None):
        path = []
        cur_pos = (len(self.__hive.map.map) - 1 - (self.__location.x if from_ is None else from_.x) // FLY_POINTS_IN_SECOND, (self.__location.y if from_ is None else from_.y) // FLY_POINTS_IN_SECOND)
        cur_location = self.__hive.map.map[cur_pos[0]][cur_pos[1]]
        target_pos = target.get_position()
        finish_pos = (len(self.__hive.map.map) - 1 - target_pos[0] // FLY_POINTS_IN_SECOND, target_pos[1] // FLY_POINTS_IN_SECOND)
        finish_location = self.__hive.map.map[finish_pos[0]][finish_pos[1]]
        
        track = self.__get_track(cur_pos, cur_location, finish_location, self.__hive.map)
        try:
            while finish_location != None:
                path.append(finish_location)
                finish_location = track[finish_location]
            path.reverse()
        except:
            pass
        return path


    def wait(self):
        self.__state = AwaitState()
        self.__turtle.up()
        self.__turtle.clear()
        self.__turtle.color(*COLOR_GENERATOR.get_inactive_state_color())
        self.take_order()
        self.__hive.impossible_orders_check()

    def fly(self, target, wait=False):
         if not len(self.__path):
             self.__path = self.build_path(target)
         self.__state = FlyingState(target, wait_for_partner=wait)
         self.__turtle.color(self.__active_color)
         self.__turtle.up()

    def next_move(self):
        if len(self.__path) > 0:
            next_step = self.__path[0]
            self.__path = self.__path[1:]
            return next_step
        return None


    def carry_to(self, path, shipment, carrying_together=False):
        self.__path = path
        self.__state = CarryingState(shipment, carry_together=carrying_together)
        self.__turtle.down()

    def take_order(self, together=False):
        orders = self.__hive.orders
        candidates = []
        if isinstance(self.__state, AwaitState) and len(orders) > 0:
            for order in orders:
                data = self.can_take_order(order, together)
                if data[0]:
                    candidates.append((order, data[1]))
            if len(candidates) > 0:
                best_candidate = min(candidates, key=lambda o: o[1])
                together = together if best_candidate[0].weight <= HEAVY_ORDER_SIDE else True
                if not together:
                    self.__hive.send_order_request(self, best_candidate)
                else:
                    self.__hive.call_for_help(self, best_candidate)

    def charge(self):
        self.__battery.charge()

    def get_charge(self):
        return self.__battery.get_charge()

    def get_location(self):
        return self.__location
    
    def set_location(self, x, y):
        self.__location.x = x
        self.__location.y = y
    
    def set_partner(self, drone):
        self.__partner = drone

    def get_partner(self):
        return self.__partner
    
    def get_state(self):
        return self.__state
    
    def get_id(self):
        return self.__id
    
    def get_order_id(self):
        return self.__order_id

    def get_station(self):
        return self.__station
    
    def get_hive(self):
        return self.__hive

    def is_low_energy(self):
        return self.__battery.is_low()
    
    def is_full_energy(self):
        return self.__battery.is_full()
    
    def can_take_order(self, order, together=False):
        path_to_order = self.build_path(order)
        path_to_order_dest = self.build_path(order.dest_pos, order.location)
        carrying_state_simulation = CarryingState(order, carry_together=together)
        possibly_taken_charge = self.calculate_battery_spending(path_to_order, (path_to_order_dest, carrying_state_simulation))
        if self.__battery.get_charge() - possibly_taken_charge >= VERY_LOW_CHARGE:
            #self.__path = path_to_order
            return (True, self.path_distance(path_to_order))
        return (False, -1)
    
    def set_state(self, state):
        if isinstance(state, (AwaitState, FlyingState, CarryingState, ChargingState, WaitForHelpState)):
            self.__state = state

    def set_order_id(self, order_id):
        self.__order_id = order_id
    
    def del_order_id(self):
        self.__order_id = None