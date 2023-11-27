import turtle

from Shared_constants import WIDTH, HEIGHT, PADDING
from Location import Location


from Drone import Drone
from Drone_hive import DroneHive
from order_obstacles import Order, Barrier, OrderObstaclesHelper
from screen import Background
from Station import Station


def screen_setup():
    main_turtle = turtle.Screen()
    main_turtle.setup(WIDTH, HEIGHT)
    main_turtle.setworldcoordinates(0-PADDING, 0-PADDING, WIDTH, HEIGHT)
    main_turtle.cv._rootwindow.resizable(False, False)
    background = Background(main_turtle)
    main_turtle.colormode(255)
    return main_turtle

def stations_setup():
    st = Station()
    st.draw()

def drones_setup():
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

def obstacles_setup(helper):

    helper.barriers.append(Barrier(20, 20, 10, 7, 6))
    helper.barriers.append(Barrier(60, 50, 10, 10, 6))
    helper.draw_items(helper.barriers)
    helper.draw_items(helper.orders)

if __name__ == "__main__":
    main_turtle = screen_setup()
    helper = OrderObstaclesHelper()
    turtle.onscreenclick(helper.on_click)

    obstacles_setup(helper)
    stations_setup()
    drones_setup()

    main_turtle.mainloop()


