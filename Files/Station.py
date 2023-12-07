import turtle
from Shared_constants import WIDTH, HEIGHT, STATION_KOEF
from Shared_Methods import round_to_fly_points
from Location import Location
from Charging_State import ChargingState

class Station:
    def __init__(self):
        self._energy = 10000
        self._width = 4 * STATION_KOEF
        self._height = 8 * STATION_KOEF
        self._location = Location(WIDTH / 2, HEIGHT / 2 + self._height / 2)
        self._places = {}
        for i in range(40):
            self._places[i] = None

    def draw(self):
        t = turtle.Turtle()
        t.hideturtle()
        t.penup()
        t.speed(0)
        t.setposition(self._location.get_position())
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
        '''Заряжает станцию, если ее заряд ниже 5 тысяч'''
        if self._energy < 5000:
            self._energy += 1

    def get_energy(self):
        '''Возвращает заряд станции'''
        return self._energy

    def get_position(self):
        '''Возвращает координаты станции'''
        return self._location.get_position()
    
    def get_location_place(self, place_id):
        '''Возвращает локацию определенного места'''
        x, y = self._location.get_position()
        x = x + ((place_id * STATION_KOEF) % self._width) + (STATION_KOEF / 2)
        y = y - (((place_id * STATION_KOEF) // (self._height + STATION_KOEF)) * 10) - STATION_KOEF / 2
        return Location(round_to_fly_points(x), round_to_fly_points(y))

    def get_places(self):
        '''Вовращает места станции ввиде словаря, где ключ - номер места, значение - id дрона'''
        return self._places

    def count_free_places(self):
        '''Вовращает количество свободных мест'''
        count = 0
        for key in self._places.keys():
            if not self._places[key]:
                count += 1
        return count
    
    def get_free_places_ids(self):
        '''Возвращает номера свободных мест'''
        ids = []
        for k in self._places.keys():
            if not self._places[k]:
                ids.append(k)
        return ids
    
    def charge_drone(self, drone):
        '''Пополняет заряд дрона за счет заряда станции'''
        if not drone.is_full_energy() and self._energy > 0:
            drone.charge()
            self._energy -= 1
        else:
            drone.wait()

    def set_drone(self, drone):
        '''Присваивает дрону свободное место, если свободных мест нет, то переводит дрон в режим ожидания'''
        if self.count_free_places() > 0:
            keys = list(self._places.keys())
            index = list(self._places.values()).index(None)
            self._places[keys[index]] = drone.get_id()
            drone.set_state(ChargingState)
        else:
            drone.wait()

    def set_drone(self, drone, place_id):
        self._places[place_id] = drone.get_id()

    def remove_drone(self, drone):
        '''Убирает дрон со своего места'''
        for k in self._places.keys():
            if self._places[k] == drone.get_id():
                self._places[k] = None
    

if __name__ == "__main__":

    screen = turtle.Screen()
    screen.setup(WIDTH + 4, HEIGHT + 8)
    screen.setworldcoordinates(0, 0, WIDTH, HEIGHT)
    screen.title("Управление дронами")

    st = Station()
    st.draw()
    turtle.done()
