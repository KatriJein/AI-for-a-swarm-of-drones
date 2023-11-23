import turtle

from Files.Additional.Constants import ID_GENERATOR, COLOR_GENERATOR, BATTERY_CHARGE, FLIGHT_ALTITUDE, WIDTH, LENGTH
from Files.Additional.Location import Location
from Files.Drone.Battery import Battery
from Files.Drone_States import Await_State, Carrying_State, Flying_State

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


class Drone:
    def __init__(self, width=WIDTH, length=LENGTH, flight_altitude=FLIGHT_ALTITUDE):
        self.__id = ID_GENERATOR.get_id()
        self.__width = width
        self.__length = length
        self.__location = Location()
        self.__battery = Battery(charge=BATTERY_CHARGE)
        self.__state = Await_State.AwaitState()
        self.__flight_altitude = flight_altitude
        self.__order_id = None

        self.__set_graphics()

    def __set_graphics(self):
        self.__turtle = turtle.Turtle(shape="circle")
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
        self.__state = Await_State.AwaitState()
        self.__turtle.up()
        self.__turtle.color(*COLOR_GENERATOR.get_inactive_state_color())

    def fly_to(self, target):
        self.__state = Flying_State.FlyingState(target)
        self.__turtle.color(self.__active_color)
        self.__turtle.up()

    def carry_to(self, shipment, target):
        self.__state = Carrying_State.CarryingState(shipment, target)
        self.__turtle.down()

    def view_order(self, order):
        return self.can_take_order(order)

    def take_order(self, order):
        self.__order_id = order.get_id()
        self.fly_to(order)

    def get_location(self):
        return self.__location
    
    def get_state(self):
        return self.__state
    
    def get_id(self):
        return self.__id

    def is_low_energy(self):
        return self.__battery.is_low()
    
    def can_take_order(self, order):
        return True
    
    def set_state(self, state):
        if isinstance(state, (Await_State.AwaitState, Flying_State.FlyingState, Carrying_State.CarryingState)):
            self.__state = state



if __name__ == "__main__":
    main_turtle = turtle.Screen()
    main_turtle.setworldcoordinates(0, 0, 1000, 1000)
    main_turtle.colormode(255)
    hive = DroneHive()
    drone = Drone()
    drone1 = Drone()
    hive.add_drone(drone)
    hive.add_drone(drone1)
    drone.fly_to(Location(2, 4))
    drone1.fly_to(Location(4, 0))
    for i in range(150):
        hive.act()
        hive.draw()
    drone.wait()
    main_turtle.mainloop()


