from Shared_constants import WIDTH, HEIGHT, PADDING, START_X, START_Y, FLY_POINTS_IN_SECOND
from Location import Location

class Map:
    def __init__(self):
        self.__x_values = [i for i in range(START_X, WIDTH + 1) if i % FLY_POINTS_IN_SECOND == 0]
        self.__y_values = [i for i in range(START_Y, HEIGHT + 1) if i % FLY_POINTS_IN_SECOND == 0]
        self.map = self.__create_map()

    def __create_map(self):
        map_ = []
        for x_value in self.__x_values:
            row = []
            for y_value in self.__y_values:
                row.append(Location(x_value, y_value))
            map_.insert(0, row)
        return map_
    
