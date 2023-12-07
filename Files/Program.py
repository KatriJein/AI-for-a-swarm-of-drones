import turtle

from Shared_constants import WIDTH, HEIGHT, PADDING, START_X, START_Y
from Location import Location


from Drone import Drone
from Drone_hive import DroneHive
from order_obstacles import Barrier, OrderObstaclesHelper
from screen import Background
from Station import Station
from Map import Map


def screen_setup():
    main_turtle = turtle.Screen()
    main_turtle.setup(WIDTH, HEIGHT)
    main_turtle.setworldcoordinates(START_X, START_Y, WIDTH, HEIGHT)
    main_turtle.cv._rootwindow.resizable(False, False)
    background = Background(main_turtle)
    main_turtle.colormode(255)
    return main_turtle

# def stations_setup():
#     st = Station()
#     st.draw()

def drones_setup(hive):
    drone = Drone(hive, st)
    drone1 = Drone(hive, st)
    drone2 = Drone(hive, st)
    drone3 = Drone(hive, st)
    hive.add_drone(drone)
    hive.add_drone(drone1)
    hive.add_drone(drone2)
    hive.add_drone(drone3)

def main_cycle(hive):
    while True:
        hive.act()
        hive.draw()
        helper.update()
        main_turtle.update()

def obstacles_setup(helper, map_):

    helper.barriers.append(Barrier(Location(20, 20, 6), 15, 20, map_))
    helper.barriers.append(Barrier(Location(60, 50, 6), 13, 33, map_))
    helper.barriers.append(Barrier(Location(30, 30, 6), 10, 10, map_))
    helper.barriers.append(Barrier(Location(10, 20, 6), 10, 10, map_))
    helper.draw_items(helper.barriers)
    helper.draw_items(helper.orders)

if __name__ == "__main__":
    main_turtle = screen_setup()
    main_turtle.tracer(10, 0)
    map_ = Map()
    hive = DroneHive(map_)
    helper = OrderObstaclesHelper(hive)
    turtle.onscreenclick(helper.on_click)

    obstacles_setup(helper, map_)
    # stations_setup()
    st = Station()
    st.draw()
    drones_setup(hive)
    main_turtle.update()
    main_cycle(hive)

    main_turtle.mainloop()


