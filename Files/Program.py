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

HANDY_MODE = True
plan = ORDER_PLAN

def add_order_plan():
    global plan
    plan += 1

def decrease_order_plan():
    global plan
    if plan - helper.get_spawned_quantity() > 1:
        plan -= 1

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
    while len(hive.delivered_orders) < plan or not hive.are_drones_done(plan):
        hive.act()
        hive.draw()
        st.draw_update()
        st.charge()
        #hive.impossible_orders_check()
        station.charge()
        task2 = asyncio.create_task(helper.update(plan))
        await task2
        main_turtle.update()
        main_turtle.title(f"Управление дронами. Осталось недоставленных посылок: {plan - len(hive.delivered_orders)}")
    plan_turtle.clear()
    mode_turtle.clear()
    turtle.onkey(None, 'q')
    turtle.onkey(None, 's')
    turtle.onkey(None, 'w')
    turtle.onkey(None, 't')
    turtle.onkey(None, 'y')
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

def switch_mode():
    mode_turtle.clear()
    global HANDY_MODE
    if HANDY_MODE:
        turtle.onscreenclick(None)
        mode_turtle.write(f"Автоматический режим. Время появления заказа: {helper.get_spawn_time()} с.", font=("Times New Roman", 25, "bold"))
        helper.start_order_timer()
    else:
        turtle.onscreenclick(helper.on_click)
        mode_turtle.write("Ручной режим", font=("Times New Roman", 25, "bold"))
        helper.stop_order_timer()
    HANDY_MODE = not HANDY_MODE

if __name__ == "__main__":
    try:
        main_turtle = screen_setup()
        main_turtle.tracer(TRACER_LEVEL, 0)
        map_ = Map()
        st = Station(map_)
        hive = DroneHive(map_)
        helper = OrderObstaclesHelper(hive)
        mode_turtle = turtle.Turtle()
        mode_turtle.hideturtle()
        mode_turtle.speed("fastest")
        mode_turtle.color("black")
        turtle.onscreenclick(helper.on_click)
        mode_turtle.write("Ручной режим", font=("Times New Roman", 25, "bold"))
        turtle.listen()
        turtle.onkey(switch_mode, 'q')
        turtle.onkey(lambda: helper.add_spawn_time(mode_turtle), 's')
        turtle.onkey(lambda: helper.decrease_spawn_time(mode_turtle), 'w')
        turtle.onkey(add_order_plan, 't')
        turtle.onkey(decrease_order_plan, 'y')


        obstacles_setup(helper, st, map_)
        # stations_setup()
        st.draw()
        drones_setup(hive)
        main_turtle.update()
        asyncio.run(main_cycle(hive, st))

        main_turtle.mainloop()
    except Exception as e:
        print(e)


