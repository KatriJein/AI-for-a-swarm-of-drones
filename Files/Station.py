import turtle
from Shared_constants import WIDTH, HEIGHT, STATION_KOEF, ORDER_SIZE
from Shared_Methods import round_to_fly_points, save_obj_to_map
from Location import Location
from Charging_State import ChargingState
from shapely.geometry import Polygon

turtle.register_shape('Files\Images\poligon.gif')

class Station:
    def __init__(self, map_):
        self._energy = 10000
        self._width = 4 * STATION_KOEF
        self._height = 8 * STATION_KOEF
        self._location = Location(round_to_fly_points(WIDTH / 2), round_to_fly_points(HEIGHT / 2 + self._height / 2))
        self._location.z = 10 * STATION_KOEF
        self._places_coordinates = {}
        self._places_drones = {}
        self._places_count = 32
        self.places_width = self._places_count // 4
        self.places_height = self._places_count // self.places_width
        self._place_size = self._width // 4

        arr = []
        for i in range(self.places_width):
            for j in range(self.places_height):
                arr.append((i * self._place_size + self._location.x, j * self._place_size + self._location.y))

        for i in range(self._places_count):
            self._places_coordinates[i] = arr[i]

        for i in range(self._places_count):
            self._places_drones[i] = None
        
        self.polygon = Polygon([[self._location.x - ORDER_SIZE, self._location.y - ORDER_SIZE], [self._location.x + self._height + ORDER_SIZE, self._location.y - ORDER_SIZE], 
                                [self._location.x + self._height, self._location.y + self._width], [self._location.x, self._location.y + self._width]])
        self.is_deleted = False
        save_obj_to_map(self, map_)


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
        t.shape('Files\Images\poligon.gif')
        t.hideturtle()
        t.penup()
        t.speed(0)
        t.setposition(self._location.get_position())
        for i in range(self._places_count):
            t.setposition(self._places_coordinates[i])
            t.stamp()
            for j in range(4):
                t.forward(self._place_size)
                t.left(90)
            t.penup()

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
    
    def get_location(self):
        return self._location
    
    def get_location_place(self, place_id):
        '''Возвращает локацию определенного места'''
        x, y = self.get_place_coordinates(place_id)
        return Location(round_to_fly_points(x), round_to_fly_points(y))

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
            if self._places_drones[k] is None:
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
            keys = list(self._places_drones.keys())
            index = list(self._places_drones.values()).index(None)
            self._places_drones[keys[index]] = drone.get_id()
            drone.set_state(ChargingState())
        else:
            drone.wait()

    def set_drone(self, drone, place_id):
        self._places_drones[place_id] = drone.get_id()

    def __sum_minimum_delta(self, value, left_delta, right_delta):
        if abs(left_delta) > abs(right_delta):
            value += right_delta
        else:
            value += left_delta
        return value

    #def __define_best_coordinate(self, coords):
        #y_value = coords[1]
        #bounds = self.polygon.bounds
        #y_down_delta = bounds[1]  - y_value
        #y_up_delta = bounds[3]  - y_value
        #y_value = self.__sum_minimum_delta(y_value, y_down_delta, y_up_delta)
        #return round_to_fly_points(y_value + STATION_KOEF / 2)


    def remove_drone(self, drone):
        '''Убирает дрон со своего места'''
        bounds = self.polygon.bounds
        for k in self._places_drones.keys():
            if self._places_drones[k] == drone.get_id():
                self._places_drones[k] = None
        drone.set_location(round_to_fly_points(bounds[0] + (bounds[2] - bounds[0]) / 2), round_to_fly_points(bounds[1] - 10))
    

if __name__ == "__main__":

    screen = turtle.Screen()
    screen.setup(WIDTH + 4, HEIGHT + 8)
    screen.setworldcoordinates(0, 0, WIDTH, HEIGHT)
    screen.title("Управление дронами")

    st = Station()
    st.draw()
    turtle.done()
