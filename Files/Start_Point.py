from Location import Location
from Drone_Constants import FLIGHT_ALTITUDE

class StartPoint:
    def __init__(self):
        self.location = Location(580, 400, z=FLIGHT_ALTITUDE)

    def get_position(self):
        return self.location.get_position()