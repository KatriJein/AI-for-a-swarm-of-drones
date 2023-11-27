
class DroneId:
    def __init__(self):
        self.__next_id = 0
    def get_id(self):
        self.__next_id += 1
        return self.__next_id - 1