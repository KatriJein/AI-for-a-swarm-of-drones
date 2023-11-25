import turtle, random
from shapely.geometry import Polygon

WIDTH, HEIGHT = 1000, 700

screen = turtle.Screen()
screen.setup(WIDTH, HEIGHT)  
screen.setworldcoordinates(0, 0, WIDTH, HEIGHT)
screen.cv._rootwindow.resizable(False, False)
screen.title("Управление дронами")
koef = 10

class Order:
    def __init__(self, id, x, y, weight, destination_x, destination_y):
        self.id = id 
        self.x = x
        self.y = y
        self.weight = weight 
        self.dest_x = destination_x
        self.dest_y = destination_y
        # self.polygon = Polygon([[self.x - 11, self.y + 11], [self.x + 11, self.y + 11], 
        #                         [self.x + 11, self.y - 11], [self.x - 11, self.y - 11]])

    def draw(self):
            order_t = turtle.Turtle()
            order_t.penup()
            order_t.speed(0)
            order_t.color("yellow")
            order_t.shape("square")
            order_t.setposition(self.x, self.y)

class Barrier:
    def __init__(self, x, y, width, lenght, height):
        self.x = x * koef
        self.y = y * koef
        self.width = width * koef
        self.lenght = lenght * koef
        self.height = height * koef
        self.polygon = Polygon([[self.x, self.y], [self.x + self.width, self.y], 
                                [self.x + self.width, self.y - self.lenght], [self.x, self.y - self.lenght]])

    def draw(self):
            barrier_t = turtle.Turtle()
            barrier_t.hideturtle()
            barrier_t.penup()
            barrier_t.speed(0)
            barrier_t.setposition(self.x, self.y)
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


def generate_new_order(start_x, start_y, dest_x, dest_y):
    new_order = Order(
        find_max_index(),
        start_x,
        start_y,
        random.randint(10, 30000),
        dest_x,
        dest_y
    )
    orders.append(new_order)
    new_order.draw()
    
def create_polygon_for_point(x, y):
    return Polygon([[x - 11, y + 11], [x + 11, y + 11], 
                        [x + 11, y - 11], [x - 11, y - 11]])

def find_max_index():
    return max(order.id for order in orders) + 1 if orders else 0

def is_intersects_any_polygon(polygons, x, y):
    return any(p.polygon.intersects(create_polygon_for_point(x, y)) for p in polygons)

current_order = False
curr_x, curr_y = 0, 0

def on_click(x, y):
    global current_order, curr_x, curr_y

    if not current_order and not is_intersects_any_polygon(barriers, x, y):
        curr_x, curr_y = x, y
        current_order = True
    elif current_order and not is_intersects_any_polygon(barriers, x, y):
        generate_new_order(curr_x, curr_y, x, y)
        current_order = False 
        curr_x, curr_y = 0, 0 

def draw_items(arr):
    for item in arr:
        item.draw()
             
                       
orders = []
barriers = []

barriers.append(Barrier(20, 20, 10, 7, 6))
barriers.append(Barrier(60, 50, 10, 10, 6))
draw_items(barriers)
draw_items(orders)

turtle.onscreenclick(on_click)

turtle.done()