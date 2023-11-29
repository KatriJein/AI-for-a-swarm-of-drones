import turtle

from Shared_constants import WIDTH, HEIGHT, PADDING, START_X, START_Y
from Location import Location


from Drone import Drone
from Drone_hive import DroneHive
from order_obstacles import Order, Barrier, OrderObstaclesHelper
from screen import Background
from Station import Station
from Map import Map


def screen_setup():
    main_turtle = turtle.Screen()
    main_turtle.setup(WIDTH, HEIGHT)
    main_turtle.setworldcoordinates(START_X, START_Y, WIDTH, HEIGHT)
    #main_turtle.cv._rootwindow.resizable(False, False)
    background = Background(main_turtle)
    main_turtle.colormode(255)
    return main_turtle

def stations_setup():
    st = Station()
    st.draw()

def drones_setup():
    drone = Drone()
    drone1 = Drone()
    drone2 = Drone()
    drone3 = Drone()
    hive.add_drone(drone)
    hive.add_drone(drone1)
    hive.add_drone(drone2)
    hive.add_drone(drone3)
    for i in range(3500):
        hive.act()
        hive.draw()

def obstacles_setup(helper):

    helper.barriers.append(Barrier(Location(20, 20), 10, 7, 6))
    helper.barriers.append(Barrier(Location(60, 50), 10, 10, 6))
    helper.draw_items(helper.barriers)
    helper.draw_items(helper.orders)

if __name__ == "__main__":
    main_turtle = screen_setup()
    map = Map()
    hive = DroneHive(map)
    helper = OrderObstaclesHelper(hive)
    turtle.onscreenclick(helper.on_click)

    obstacles_setup(helper)
    stations_setup()
    drones_setup()

    main_turtle.mainloop()


