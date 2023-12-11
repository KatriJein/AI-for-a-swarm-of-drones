from Drone_State import DroneState

class AwaitState(DroneState):
    def __init__(self, taken_energy=0):
        super().__init__(taken_energy)

    def take_energy(self):
        return self.taken_energy_amount
        
    def act(self, drone):
        if drone.is_low_energy() and drone.get_station().count_free_places() > 0:
            place_id = drone.get_station().get_free_places_ids()[0]
            place_loc = drone.get_station().get_location_place(place_id)
            drone.get_station().set_drone(drone, place_id)
            drone.fly(place_loc)
