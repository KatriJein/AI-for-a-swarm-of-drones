import turtle

from queue import Queue

from Drone_Constants import ID_GENERATOR, COLOR_GENERATOR, BATTERY_CHARGE, FLIGHT_ALTITUDE, DRONE_WIDTH, DRONE_LENGTH
from Shared_constants import FLY_POINTS_IN_SECOND, VERY_LOW_CHARGE
from Location import Location
from Battery import Battery
from Station import Station
from order_obstacles import Barrier
from Await_State import AwaitState
from Flying_State import FlyingState
from Carrying_State import CarryingState

turtle.register_shape(".venv\Files\Images\drone.gif")

class Drone:
    def __init__(self, hive, width=DRONE_WIDTH, length=DRONE_LENGTH):
        self.__id = ID_GENERATOR.get_id()
        self.__width = width
        self.__length = length
        self.__location = Location(z=FLIGHT_ALTITUDE)
        self.__battery = Battery(charge=BATTERY_CHARGE)
        self.__state = AwaitState()
        self.__flight_altitude = self.__location.z
        self.__order_id = None
        self.__path = []
        self.__hive = hive

        self.__set_graphics()

    def __set_graphics(self):
        self.__turtle = turtle.Turtle(shape=".venv\Files\Images\drone.gif")
        self.__text_turtle = turtle.Turtle()
        self.__text_turtle.hideturtle()
        self.__text_turtle.speed("fastest")
        self.__text_turtle.color("black")
        self.__turtle.shapesize(self.__width, self.__length, 1)
        self.__turtle.speed(15)
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
        self.__text_turtle.write(f"Id: {self.__id}, charge: {round(self.__battery.get_charge(), 2)}", font=("Times New Roman", 15, "bold"))
        

    def act(self):
        self.__state.act(self)

    def take_energy(self):
        self.__battery.take_energy(self.__state.take_energy())

    def path_distance(self):
        completed_steps = 0
        for i in range(1, len(self.__path)):
            cur_loc = self.__path[i].get_position()
            prev_loc = self.__path[i - 1].get_position()
            completed_steps += abs(cur_loc[0] - prev_loc[0]) + abs(cur_loc[1] - prev_loc[1])
        return completed_steps
            
    def calculate_battery_spending(self):
        return self.__state.take_energy() * self.path_distance()
    
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
                    if next_elem in track or (self.__flight_altitude <= next_elem.z
                                               and isinstance(next_elem.obj_at_location, Barrier)):
                        continue
                    track[next_elem] = pos[0]
                    queue.put((next_elem, n_pos))
            if end in track:
                break
        
        return track


    def build_path(self, target_pos):
        self.__path = []
        cur_pos = (len(self.__hive.map.map) - 1 - self.__location.x // FLY_POINTS_IN_SECOND, self.__location.y // FLY_POINTS_IN_SECOND)
        cur_location = self.__hive.map.map[cur_pos[0]][cur_pos[1]]
        # target_pos = target.get_position()
        finish_pos = (len(self.__hive.map.map) - 1 - target_pos[0] // FLY_POINTS_IN_SECOND, target_pos[1] // FLY_POINTS_IN_SECOND)
        finish_location = self.__hive.map.map[finish_pos[0]][finish_pos[1]]
        
        track = self.__get_track(cur_pos, cur_location, finish_location, self.__hive.map)
        while finish_location != None:
            self.__path.append(finish_location)
            finish_location = track[finish_location]
        self.__path.reverse()


    def wait(self):
        self.__state = AwaitState()
        self.__turtle.up()
        self.__turtle.color(*COLOR_GENERATOR.get_inactive_state_color())
        # self.take_order(self.__hive.map)

    # def fly_to(self, target, map_):
    #     self.__state = FlyingState(target)
    #     if not len(self.__path):
    #         self.build_path(target)

    #     self.__turtle.color(self.__active_color)
    #     self.__turtle.up()

    def next_move(self):
        if len(self.__path) > 0:
            next_step = self.__path[0]
            self.__path = self.__path[1:]
            return next_step
        return None


    def carry_to(self, shipment, target):
        self.__state = CarryingState(shipment, target)
        self.__turtle.down()

    # def take_order(self, map_):
    #     orders = self.__hive.orders
    #     candidates = []
    #     if isinstance(self.__state, AwaitState) and len(orders) > 0:
    #         for order in orders:
    #             data = self.can_take_order(map_, order)
    #             if data[0]:
    #                 candidates.append((order, self.path_distance()))
    #         if len(candidates) > 0:
    #             best_candidate = min(candidates, key=lambda o: o[1])[0]
    #             self.__hive.orders.remove(best_candidate)
    #             self.__order_id = best_candidate.get_id()
    #             self.fly_to(best_candidate, map_)

    def charge(self):
        self.__battery.charge()

    def get_location(self):
        return self.__location
    
    def get_state(self):
        return self.__state
    
    def get_id(self):
        return self.__id
    
    def get_order_id(self):
        return self.__order_id

    def is_low_energy(self):
        return self.__battery.is_low()
    
    def is_full_energy(self):
        return self.__battery.is_full()
    
    def can_take_order(self, map, order):
        self.build_path(order)
        possibly_taken_charge = self.calculate_battery_spending()
        if self.__battery.get_charge() - possibly_taken_charge >= VERY_LOW_CHARGE:
            return (True, self.path_distance())
        return (False, -1)
    
    def set_state(self, state):
        if isinstance(state, (AwaitState, FlyingState, CarryingState)):
            self.__state = state

    def set_order_id(self, order_id):
        self.__order_id = order_id