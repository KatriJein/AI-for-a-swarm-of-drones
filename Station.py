import turtle

WIDTH, HEIGHT = 1000, 600

screen = turtle.Screen()
screen.setup(WIDTH + 4, HEIGHT + 8)
screen.setworldcoordinates(0, 0, WIDTH, HEIGHT)
screen.title("Управление дронами")
koef = 10


class Station:
    def __init__(self):
        self._energy = 10000
        self._width = 4 * koef
        self._height = 8 * koef
        self._x = WIDTH / 2
        self._y = HEIGHT / 2 + (self._height / 2)
        self._places = {}
        for i in range(40):
            self._places[i] = None

    def draw(self):
        t = turtle.Turtle()
        t.hideturtle()
        t.penup()
        t.speed(0)
        t.setposition(self._x, self._y)
        t.color("red")
        t.pendown()
        t.begin_fill()
        for i in range(2):
            t.forward(self._width)
            t.right(90)
            t.forward(self._height)
            t.right(90)
        t.end_fill()

    def charge(self):
        if self._energy < 5000:
            while self._energy < 10000:
                self._energy += 1

    def get_energy(self):
        return self._energy

    def get_position(self):
        return self._x, self._y

    def get_places(self):
        return self._places

    def get_free_places(self):
        count = 0
        for key in self._places.keys():
            if not self._places[key]:
                count += 1
        return count

    def charge_drone(self, drone):
        while (not drone.is_full_energy()) and self._energy > 0:
            drone.charge()
            self._energy -= 1


st = Station()
st.draw()
turtle.done()
