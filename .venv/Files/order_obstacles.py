import turtle, random
from shapely.geometry import Polygon
from Location import Location
from Shared_constants import WIDTH, HEIGHT, BARRIER_KOEF, FLY_POINTS_IN_SECOND

class Order:
    def __init__(self, id, pos, weight, dest_pos):
        self.id = id 
        self.location = pos
        self.weight = weight 
        self.dest_pos = dest_pos
        # self.polygon = Polygon([[self.x - 11, self.y + 11], [self.x + 11, self.y + 11], 
        #                         [self.x + 11, self.y - 11], [self.x - 11, self.y - 11]])

    def draw(self):
            order_t = turtle.Turtle()
            order_t.penup()
            order_t.speed(0)
            order_t.color("yellow")
            order_t.shape("square")
            order_t.setposition(self.location.get_position())

    def get_position(self):
        return self.location.get_position()
    
    def get_id(self):
        return self.id


class Barrier:
    def __init__(self, pos, width, lenght, height):
        self.pos = pos
        self.pos.x *= BARRIER_KOEF
        self.pos.y *= BARRIER_KOEF
        self.width = width * BARRIER_KOEF
        self.lenght = lenght * BARRIER_KOEF
        self.height = height * BARRIER_KOEF
        self.polygon = Polygon([[self.pos.x, self.pos.y], [self.pos.x + self.width, self.pos.y], 
                                [self.pos.x + self.width, self.pos.y - self.lenght], [self.pos.x, self.pos.y - self.lenght]])

    def draw(self):
            barrier_t = turtle.Turtle()
            barrier_t.hideturtle()
            barrier_t.penup()
            barrier_t.speed(0)
            barrier_t.setposition(self.pos.get_position())
            barrier_t.color("black")
            barrier_t.pendown()
            barrier_t.begin_fill()
            for i in range(2):
                barrier_t.forward(self.width)
                barrier_t.right(90)
                barrier_t.forward(self.lenght)
                if i == 0:
                    barrier_t.right(90)
            barrier_t.end_fill()


class OrderObstaclesHelper:
    def __init__(self, hive):
        self.__current_order = False
        self.__curr_x = 0
        self.__curr_y = 0
        self.__hive = hive
        self.barriers = []
        self.orders = []

    def generate_new_order(self, start_x, start_y, dest_x, dest_y):
        new_order = Order(
            self.find_max_index(),
            Location(start_x, start_y),
            random.randint(10, 30000),
            Location(dest_x, dest_y)
        )
        self.orders.append(new_order)
        new_order.draw()
        self.__hive.set_order(new_order)
        
    def create_polygon_for_point(self, x, y):
        return Polygon([[x - 11, y + 11], [x + 11, y + 11], 
                            [x + 11, y - 11], [x - 11, y - 11]])

    def find_max_index(self):
        return max(order.id for order in self.orders) + 1 if self.orders else 0

    def is_intersects_any_polygon(self, polygons, x, y):
        return any(p.polygon.intersects(self.create_polygon_for_point(x, y)) for p in polygons)

    def on_click(self, x, y):
        if not self.__current_order and not self.is_intersects_any_polygon(self.barriers, x, y):
            self.__curr_x, self.__curr_y = int(x) - int(x) % FLY_POINTS_IN_SECOND, int(y) - int(y) % FLY_POINTS_IN_SECOND
            self.__current_order = True
        elif self.__current_order and not self.is_intersects_any_polygon(self.barriers, x, y):
            self.generate_new_order(self.__curr_x, self.__curr_y, x, y)
            self.__current_order = False 
            self.__curr_x, self.__curr_y = 0, 0 

    def draw_items(self, arr):
        for item in arr:
            item.draw()


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