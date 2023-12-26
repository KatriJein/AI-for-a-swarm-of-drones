import turtle, random, os
from time import time
from shapely.geometry import Polygon
from Location import Location
from Shared_constants import WIDTH, HEIGHT, BARRIER_KOEF, FLY_POINTS_IN_SECOND, ORDER_SIZE, SPAWN_ORDER_TIME, ORDER_PLAN, MIN_ORDER_SIZE, MAX_ORDER_SIZE
from Shared_Methods import get_corresponding_location_in_map, round_to_fly_points, save_obj_to_map, create_free_map_coordinates
from Station import Station

order_path = os.path.join("Files", "Images", "order.gif")
plan = ORDER_PLAN

def get_path_to_build_img(id):
    return f'Files\Images\Buildings\Building{id}.gif'

turtle.register_shape(order_path)
turtle.register_shape(get_path_to_build_img(1))
turtle.register_shape(get_path_to_build_img(2))
turtle.register_shape(get_path_to_build_img(3))
turtle.register_shape(get_path_to_build_img(4))
turtle.register_shape(get_path_to_build_img(5))
turtle.register_shape(get_path_to_build_img(6))

squares = {
    81: ((90, 90), get_path_to_build_img(1)),
    45: ((150, 30), get_path_to_build_img(2)),
    88: ((80, 110), get_path_to_build_img(3)),
    150: ((150, 100), get_path_to_build_img(4)),
    39: ((30, 130), get_path_to_build_img(5)),
    135: ((90, 150), get_path_to_build_img(6))
}

class Order:
    def __init__(self, id, pos, weight, dest_pos):
        self.id = id 
        self.location = pos
        self.weight = weight 
        self.dest_pos = dest_pos
        self.turtle = turtle.Turtle(shape=order_path)
        self.is_deleted = False
        self.deliver_time = None

    def draw(self):
        self.turtle.penup()
        self.turtle.speed(0)
        self.turtle.setposition(self.location.get_position())
        self.text_turtle = turtle.Turtle()
        self.text_turtle.penup()
        self.text_turtle.hideturtle()
        self.text_turtle.speed("fastest")
        self.text_turtle.color("black")
        loc = self.location.get_position()
        text_pos = (loc[0] - 50, loc[1] + 12)
        self.text_turtle.goto(text_pos)
        self.text_turtle.write(f'Вес: {round(self.weight / 1000, 1)} кг', font=("Times New Roman", 15, "bold"))

    def taken_by_drone(self):
        self.turtle.hideturtle()
        self.text_turtle.clear()

    def untaken_by_drone(self):
        self.turtle.showturtle()
        self.text_turtle.write(f'Вес: {round(self.weight / 1000, 1)} кг', font=("Times New Roman", 15, "bold"))

    def delivered_by_drone(self):
        self.turtle.speed(0)
        self.turtle.goto(self.dest_pos.get_position()[0], self.dest_pos.get_position()[1])
        text_pos = (self.dest_pos.get_position()[0] - 50, self.dest_pos.get_position()[1] + 12)
        self.text_turtle.goto(text_pos)
        self.location = self.dest_pos
        self.turtle.showturtle()
        #self.text_turtle.write(f'Вес: {round(self.weight / 1000, 1)} кг', font=("Times New Roman", 15, "bold"))
        self.is_deleted = True
        self.deliver_time = time()

    def get_position(self):
        return self.location.get_position()
    
    def get_id(self):
        return self.id


class Barrier:
    def __init__(self, pos, square, map_):
        self.pos = pos
        self.pos.x = round_to_fly_points(self.pos.x * BARRIER_KOEF)
        self.pos.y = round_to_fly_points(self.pos.y * BARRIER_KOEF)
        self.pos.z *= BARRIER_KOEF
        (self.width, self.lenght), self.path_to_img = squares[square]
        self.turtle = turtle.Turtle(shape=self.path_to_img)
        self.is_deleted = False
        self.polygon = Polygon([[self.pos.x, self.pos.y], [self.pos.x + self.width, self.pos.y], 
                                [self.pos.x + self.width, self.pos.y - self.lenght], [self.pos.x, self.pos.y - self.lenght]])
        save_obj_to_map(self, map_)

    def draw(self):
        self.turtle.penup()
        self.turtle.speed(0)
        self.turtle.setposition(self.get_center_pos())
            # self.turtle.hideturtle()
            # self.turtle.penup()
            # self.turtle.speed(0)
            # self.turtle.setposition(self.pos.get_position())
            # self.turtle.color("black")
            # self.turtle.pendown()
            # self.turtle.begin_fill()
            # for i in range(2):
            #     self.turtle.forward(self.width)
            #     self.turtle.right(90)
            #     self.turtle.forward(self.lenght)
            #     if i == 0:
            #         self.turtle.right(90)
            # self.turtle.end_fill()

    def get_location(self):
        return self.pos

    def get_center_pos(self):
        x, y = self.pos.get_position()
        return (x + self.width / 2, y - self.lenght / 2)

    
class OrderObstaclesHelper:
    def __init__(self, hive):
        self.__current_order = False
        self.__curr_x = 0
        self.__curr_y = 0
        self.__hive = hive
        self.barriers = []
        self.orders = []
        self.__start_timer = False
        self.__cur_time = 0


    def generate_new_order(self, start_x, start_y, dest_x, dest_y):
        new_order = Order(
            self.find_max_index(),
            Location(start_x, start_y),
            random.randint(MIN_ORDER_SIZE, MAX_ORDER_SIZE),
            Location(dest_x, dest_y)
        )
        self.orders.append(new_order)
        new_order.draw()
        self.__hive.set_order(new_order)
        
    def create_polygon_for_point(self, x, y):
        return Polygon([[x - ORDER_SIZE - FLY_POINTS_IN_SECOND, y + ORDER_SIZE + FLY_POINTS_IN_SECOND], [x + ORDER_SIZE + FLY_POINTS_IN_SECOND, y + ORDER_SIZE + FLY_POINTS_IN_SECOND], 
                            [x + ORDER_SIZE + FLY_POINTS_IN_SECOND, y - ORDER_SIZE - FLY_POINTS_IN_SECOND], [x - ORDER_SIZE - FLY_POINTS_IN_SECOND, y - ORDER_SIZE - FLY_POINTS_IN_SECOND]])

    def start_order_timer(self):
        self.__start_timer = True
        self.__cur_time = time()
    
    async def __order_timer_check(self):
        if not self.__start_timer:
            return
        if time() - self.__cur_time >= SPAWN_ORDER_TIME:
            await self.__spawn_order_automatic()
            self.__cur_time = time()
            

    async def __spawn_order_automatic(self):
        global plan
        x1, y1 = await create_free_map_coordinates(self)
        self.on_click(x1, y1)
        x2, y2 = await create_free_map_coordinates(self)
        self.on_click(x2, y2)


    def find_max_index(self):
        return max(order.id for order in self.orders) + 1 if self.orders else 0

    def is_intersects_any_polygon(self, polygons, x, y):
        return any(p.polygon.intersects(self.create_polygon_for_point(x, y)) for p in polygons)

    def on_click(self, x, y):
        global plan
        if plan > 0:
            if x >= 0 and x <= self.__hive.map.x_max and y >= 0 and y <= self.__hive.map.y_max:
                if not self.__current_order and not self.is_intersects_any_polygon(self.barriers, x, y):
                    self.__curr_x, self.__curr_y = round_to_fly_points(x), round_to_fly_points(y)
                    self.__current_order = True
                elif self.__current_order and not self.is_intersects_any_polygon(self.barriers, x, y):
                    self.generate_new_order(self.__curr_x, self.__curr_y, round_to_fly_points(x), round_to_fly_points(y))
                    self.__current_order = False 
                    self.__curr_x, self.__curr_y = 0, 0
                    plan -= 1 

    def draw_items(self, arr):
        for item in arr:
            if not isinstance(item, Station):
                if item.is_deleted:
                    arr.remove(item)
                else:
                    item.draw()

    async def update(self):
        global plan
        if plan > 0:
            await self.__order_timer_check()
        for i in range(len(self.orders) - 1, -1, -1):
            if self.orders[i].is_deleted:
                if time() - self.orders[i].deliver_time > 1:
                    self.orders[i].turtle.hideturtle()
                    self.orders[i].text_turtle.clear()
                    del self.orders[i]



if __name__ == "__main__":

    screen = turtle.Screen()
    screen.setup(WIDTH, HEIGHT)  
    screen.setworldcoordinates(0, 0, WIDTH, HEIGHT)
    screen.cv._rootwindow.resizable(False, False)
    screen.title("Управление дронами")

    helper = OrderObstaclesHelper()

    helper.barriers.append(Barrier(Location(20, 20), 10, 7, 6))
    helper.barriers.append(Barrier(Location(60, 50), 10, 10, 6))
    helper.draw_items(helper.barriers)
    helper.draw_items(helper.orders)

    turtle.onscreenclick(helper.on_click)

    turtle.done()