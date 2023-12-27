import turtle
import asyncio
from Shared_constants import WIDTH, HEIGHT, PADDING, START_X, START_Y, DRONES_QUANTITY, TRACER_LEVEL, ORDER_PLAN
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
    main_turtle.title("Управление дронами")
    background = Background(main_turtle)
    main_turtle.colormode(255)
    return main_turtle

# def stations_setup():
#     st = Station()
#     st.draw()

def drones_setup(hive):
    for i in range(DRONES_QUANTITY):
        hive.add_drone(Drone(hive, st))


async def main_cycle(hive, station):
    plan_turtle = turtle.Turtle()
    plan_turtle.hideturtle()
    plan_turtle.speed("fastest")
    plan_turtle.color("black")
    while len(hive.delivered_orders) < ORDER_PLAN or not hive.are_drones_done():
        hive.act()
        hive.draw()
        st.draw_update()
        st.charge()
        #hive.impossible_orders_check()
        station.charge()
        task2 = asyncio.create_task(helper.update())
        await task2
        main_turtle.update()
        main_turtle.title(f"Управление дронами. Осталось недоставленных посылок: {ORDER_PLAN - len(hive.delivered_orders)}")
    plan_turtle.clear()
    main_turtle.title(f"Управление дронами. План выполнен!")
    plan_turtle.write(f"План выполнен!", font=("Times New Roman", 25, "bold"))

def obstacles_setup(helper, station, map_):

    helper.barriers.append(Barrier(Location(20, 20, 6), 81, map_))
    helper.barriers.append(Barrier(Location(70, 50, 6), 88, map_))
    helper.barriers.append(Barrier(Location(30, 30, 6), 45, map_))
    helper.barriers.append(Barrier(Location(50, 20, 6), 150, map_))
    helper.barriers.append(Barrier(Location(10, 60, 6), 135, map_))
    helper.barriers.append(Barrier(Location(80, 20, 6), 39, map_))
    helper.barriers.append(station)
    helper.draw_items(helper.barriers)
    helper.draw_items(helper.orders)

if __name__ == "__main__":
    main_turtle = screen_setup()
    main_turtle.tracer(TRACER_LEVEL, 0)
    map_ = Map()
    st = Station(map_)
    hive = DroneHive(map_)
    helper = OrderObstaclesHelper(hive)
    #первая строчка для ручной установки заказа, вторая для автоматической
    turtle.onscreenclick(helper.on_click)
    #helper.start_order_timer()

    obstacles_setup(helper, st, map_)
    # stations_setup()
    st.draw()
    drones_setup(hive)
    main_turtle.update()
    asyncio.run(main_cycle(hive, st))

    main_turtle.mainloop()


