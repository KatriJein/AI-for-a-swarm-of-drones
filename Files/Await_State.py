from Drone_State import DroneState
from Shared_constants import WAIT_TIME, CHARGE_SIDE_IF_NOTHING_TO_DO
from time import time

class AwaitState(DroneState):
    def __init__(self, taken_energy=0):
        super().__init__(taken_energy)
        self.__cur_time = time()

    def take_energy(self):
        return self.taken_energy_amount
    
    def __get_ready_for_charging(self, drone):
        place_id = drone.get_station().get_free_places_ids()[0]
        place_loc = drone.get_station().get_location_place(place_id)
        drone.get_station().set_drone(drone, place_id)
        drone.fly(place_loc)
        
    def act(self, drone):
        if drone.is_low_energy() and drone.get_station().count_free_places() > 0:
            self.__get_ready_for_charging(drone)
            return
        delta = time() - self.__cur_time
        if delta > WAIT_TIME:
            drone.take_order()
            drone.get_hive().impossible_orders_check()
            if isinstance(drone.get_state(), AwaitState) and drone.get_charge() < CHARGE_SIDE_IF_NOTHING_TO_DO and drone.get_station().count_free_places() > 0:
                self.__get_ready_for_charging(drone)
            self.__cur_time = time()
        
