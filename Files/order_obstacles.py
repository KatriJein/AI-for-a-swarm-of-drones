
import turtle, random, os
import time
from shapely.geometry import Polygon
from Location import Location
from Shared_constants import WIDTH, HEIGHT, BARRIER_KOEF, FLY_POINTS_IN_SECOND
from Shared_Methods import get_corresponding_location_in_map, round_to_fly_points

order_path = os.path.join("Files", "Images", "order.gif")
turtle.register_shape(order_path)

turtle.register_shape('Files\Images\Buildings\Building1.gif')
turtle.register_shape('Files\Images\Buildings\Building2.gif')
turtle.register_shape('Files\Images\Buildings\Building3.gif')
turtle.register_shape('Files\Images\Buildings\Building4.gif')
turtle.register_shape('Files\Images\Buildings\Building5.gif')
turtle.register_shape('Files\Images\Buildings\Building6.gif')

buildings_paths = {
    (90, 90): 'Files\Images\Buildings\Building1.gif',
    (150, 30): 'Files\Images\Buildings\Building2.gif',
    (80, 110): 'Files\Images\Buildings\Building3.gif',
    (150, 100): 'Files\Images\Buildings\Building4.gif',
    (30, 130): 'Files\Images\Buildings\Building5.gif',
    (90, 150): 'Files\Images\Buildings\Building6.gif',    
}

class Order:
    def __init__(self, id, pos, weight, dest_pos):
        self.id = id 
        self.location = pos
        self.weight = weight 
        self.dest_pos = dest_pos
        self.turtle = turtle.Turtle(shape=order_path)
        self.is_deleted = False
        # self.polygon = Polygon([[self.x - 11, self.y + 11], [self.x + 11, self.y + 11], 
        #                         [self.x + 11, self.y - 11], [self.x - 11, self.y - 11]])

    def draw(self):
        self.turtle.penup()
        self.turtle.speed(0)
        self.turtle.setposition(self.location.get_position())

    def taken_by_drone(self):
        self.turtle.hideturtle()

    def delivered_by_drone(self):
        self.turtle.speed(0)
        self.turtle.goto(self.dest_pos.get_position()[0], self.dest_pos.get_position()[1])
        self.location = self.dest_pos
        self.turtle.showturtle()
        #self.turtle.hideturtle()
        #self.turtle.clear()
        self.is_deleted = True

    def get_position(self):
        return self.location.get_position()
    
    def get_id(self):
        return self.id


class Barrier:
    def __init__(self, pos, width, lenght, map_):
        self.pos = pos
        self.pos.x = round_to_fly_points(self.pos.x * BARRIER_KOEF)
        self.pos.y = round_to_fly_points(self.pos.y * BARRIER_KOEF)
        self.pos.z *= BARRIER_KOEF
        self.width = width * BARRIER_KOEF
        self.lenght = lenght * BARRIER_KOEF
        self.turtle = turtle.Turtle()
        self.is_deleted = False
        self.polygon = Polygon([[self.pos.x, self.pos.y], [self.pos.x + self.width, self.pos.y], 
                                [self.pos.x + self.width, self.pos.y - self.lenght], [self.pos.x, self.pos.y - self.lenght]])
        self.__save_barrier_on_map(map_)

    def __save_barrier_on_map(self, map_):
        pol_bounds = self.polygon.bounds
        pol_bounds = [int(b) for b in pol_bounds]
        x_values = [i for i in range(pol_bounds[0] - FLY_POINTS_IN_SECOND, pol_bounds[2] + FLY_POINTS_IN_SECOND) if i % FLY_POINTS_IN_SECOND == 0]
        y_values = [i for i in range(pol_bounds[1] - FLY_POINTS_IN_SECOND, pol_bounds[3] + FLY_POINTS_IN_SECOND) if i % FLY_POINTS_IN_SECOND == 0]
        for x in x_values:
            for y in y_values:
                loc = get_corresponding_location_in_map(map_, (x,y))
                loc.z = self.pos.z
                loc.obj_at_location = self

    def draw(self):
            self.turtle.hideturtle()
            self.turtle.penup()
            self.turtle.speed(0)
            self.turtle.setposition(self.pos.get_position())
            self.turtle.color("black")
            self.turtle.pendown()
            self.turtle.begin_fill()
            for i in range(2):
                self.turtle.forward(self.width)
                self.turtle.right(90)
                self.turtle.forward(self.lenght)
                if i == 0:
                    self.turtle.right(90)
            self.turtle.end_fill()

    


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
            self.__curr_x, self.__curr_y = round_to_fly_points(x), round_to_fly_points(y)
            self.__current_order = True
        elif self.__current_order and not self.is_intersects_any_polygon(self.barriers, x, y):
            self.generate_new_order(self.__curr_x, self.__curr_y, round_to_fly_points(x), round_to_fly_points(y))
            self.__current_order = False 
            self.__curr_x, self.__curr_y = 0, 0 

    def draw_items(self, arr):
        for item in arr:
            if item.is_deleted:
                arr.remove(item)
            else:
                item.draw()

    def update(self):
        pass


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