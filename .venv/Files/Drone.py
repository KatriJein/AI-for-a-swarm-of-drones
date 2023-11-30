import turtle

from Drone_Constants import ID_GENERATOR, COLOR_GENERATOR, BATTERY_CHARGE, FLIGHT_ALTITUDE, DRONE_WIDTH, DRONE_LENGTH
from Location import Location
from Battery import Battery
from Await_State import AwaitState
from Flying_State import FlyingState
from Carrying_State import CarryingState

turtle.register_shape(".venv\Files\Images\drone.gif")

class Drone:
    def __init__(self, width=DRONE_WIDTH, length=DRONE_LENGTH, flight_altitude=FLIGHT_ALTITUDE):
        self.__id = ID_GENERATOR.get_id()
        self.__width = width
        self.__length = length
        self.__location = Location()
        self.__battery = Battery(charge=BATTERY_CHARGE)
        self.__state = AwaitState()
        self.__flight_altitude = flight_altitude
        self.__order_id = None

        self.__set_graphics()

    def __set_graphics(self):
        self.__turtle = turtle.Turtle(shape=".venv\Files\Images\drone.gif")
        self.__turtle.shapesize(self.__width, self.__length, 1)
        self.__turtle.speed(2)
        self.__turtle.up()
        self.__turtle.setposition(self.__location.get_position())
        self.__turtle.color(*COLOR_GENERATOR.get_inactive_state_color())
        self.__active_color = COLOR_GENERATOR.generate_color()

    def draw(self):
        self.__turtle.goto(self.__location.get_position())

    def act(self):
        self.__state.act(self)

    def take_energy(self):
        self.__battery.take_energy(self.__state.take_energy())

    def distance_to(self, target):
        return 0

    def wait(self):
        self.__state = AwaitState()
        self.__turtle.up()
        self.__turtle.color(*COLOR_GENERATOR.get_inactive_state_color())

    def fly_to(self, target):
        self.__state = FlyingState(target)
        self.__turtle.color(self.__active_color)
        self.__turtle.up()

    def carry_to(self, shipment, target):
        self.__state = CarryingState(shipment, target)
        self.__turtle.down()

    def view_order(self, order):
        return self.can_take_order(order)

    def take_order(self, order):
        self.__order_id = order.get_id()
        self.fly_to(order)

    def charge(self):
        self.__battery.charge()

    def get_location(self):
        return self.__location
    
    def get_state(self):
        return self.__state
    
    def get_id(self):
        return self.__id

    def is_low_energy(self):
        return self.__battery.is_low()
    
    def is_full_energy(self):
        return self.__battery.is_full()
    
    def can_take_order(self, order):
        return True
    
    def set_state(self, state):
        if isinstance(state, (AwaitState, FlyingState, CarryingState)):
            self.__state = state