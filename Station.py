
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
        self._width = 8 * koef
        self._height = 4 * koef
        self._x = WIDTH / 2 - self._width
        self._y = HEIGHT / 2 - self._height / 2
        self._places_coordinates = {}
        self._places_drones = {}
        self._places_count = 32
        self.places_width = self._places_count // 4
        self.places_height = self._places_count // self.places_width
        self._place_size = self._width // 4

        arr = []
        for i in range(self.places_width):
            for j in range(self.places_height):
                arr.append((i * self._place_size + self._x, j * self._place_size + self._y))

        for i in range(self._places_count):
            self._places_coordinates[i] = arr[i]

        for i in range(self._places_count):
            self._places_drones[i] = None

    def charge(self):
        '''Заряжает станцию, если ее заряд ниже 5 тысяч'''
        if self._energy < 5000:
            while self._energy < 10000:
                self._energy += 1

    def get_energy(self):
        '''Возвращает заряд станции'''
        return self._energy

    def get_position(self):
        '''Возвращает координаты станции'''
        return self._x, self._y

    def get_places_coordinates(self):
        '''Возврщает словарь, ключ - номер места, значение - левые нижние координаты места'''
        return self._places_coordinates

    def get_place_coordinates(self, place_id):
        '''Возвращает координаты определенного места'''
        return self._places_coordinates[place_id]

    def get_drone_place_coordinates(self, drone_id):
        '''Возвращает координаты места дрона по индексу последнего'''
        return self._places_coordinates[list(self._places_drones.values()).index(drone_id)]

    def draw(self):
        '''Отрисовка станции'''
        t = turtle.Turtle()
        t.hideturtle()
        t.penup()
        t.speed(0)
        t.color('black')
        t.setposition(self._x, self._y)
        t.fillcolor('yellow')
        for i in range(self._places_count):
            t.setposition(self._places_coordinates[i])
            t.pendown()
            t.begin_fill()
            for j in range(4):
                t.forward(self._place_size)
                t.left(90)
            t.end_fill()
            t.penup()

    def get_places_drones(self):
        '''Вовращает места станции ввиде словаря, где ключ - номер места, значение - id дрона'''
        return self._places_drones

    def count_free_places(self):
        '''Вовращает количество свободных мест'''
        count = 0
        for key in self._places_drones.keys():
            if not self._places_drones[key]:
                count += 1
        return count

    def get_free_places_ids(self):
        '''Возвращает номера свободных мест'''
        ids = []
        for k in self._places_drones.keys():
            if not self._places_drones[k]:
                ids.append(k)
        return ids

    def charge_drone(self, drone):
        '''Пополняет заряд дрона за счет заряда станции'''
        while (not drone.is_full_energy()) and self._energy > 0:
            drone.charge()
            self._energy -= 1

    def set_drone(self, drone):
        '''Присваивает дрону свободное место, если свободных мест нет, то переводит дрон в режим ожидания'''
        if self.count_free_places() > 0:
            keys = list(self._places_drones.keys())
            index = list(self._places_drones.values()).index(None)
            self._places_drones[keys[index]] = drone.get_id()
        else:
            drone.wait()

    def remove_drone(self, drone):
        '''Убирает дрон со своего места'''
        for k in self._places_drones.keys():
            if self._places_drones[k] == drone.get_id():
                self._places_drones[k] = None

st = Station()
st.draw()
turtle.done()
