import turtle

WIDTH, HEIGHT = 1000, 600

screen = turtle.Screen()
screen.setup(WIDTH + 4, HEIGHT + 8)  # запас на границы
screen.setworldcoordinates(0, 0, WIDTH, HEIGHT)
screen.title("Управление дронами")
koef = 10

class Order:
    def __init__(self, id, x, y, weight, destination_x, destination_y):
        self.id = id 
        self.x = x * koef
        self.y = y * koef
        self.weight = weight 
        self.dest_x = destination_x * koef
        self.dest_y = destination_y * koef

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
            
            
ord = Order(1, 10, 10, 5, 25, 30)
bar = Barrier(10, 10, 10, 7, 6)
bar2 = Barrier(60, 50, 10, 10, 6)
ord.draw()
bar.draw()
bar2.draw()

turtle.done()