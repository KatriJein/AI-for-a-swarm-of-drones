
from Drone_State import DroneState
from time import time
from Shared_constants import WAIT_FOR_PARTNER_TIME

class WaitForHelpState(DroneState):
    def __init__(self, path, order, taken_energy=0):
        super().__init__(taken_energy)
        self.__path = path
        self.__order = order
        self.__cur_time = time()
    
    def take_energy(self):
        return self.taken_energy_amount
    
    def act(self, drone):
        partner = drone.get_partner()
        if isinstance(partner.get_state(), WaitForHelpState):
            drone.carry_to(self.__path, self.__order, carrying_together=True)
            partner.carry_to(self.__path, self.__order, carrying_together=True)
