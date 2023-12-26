import math
from Shared_constants import ENERGY_LEVEL_TO_CHARGE
USUAL_CHARGE = 100
LOW_LEVEL_SIDE = 20

class Battery:
    def __init__(self, charge=USUAL_CHARGE):
        self.__charge = charge

    def take_energy(self, amount):
        self.__charge -= amount

    def is_low(self):
        return self.__charge < ENERGY_LEVEL_TO_CHARGE
    
    def is_full(self):
        return self.__charge == USUAL_CHARGE
    
    def get_charge(self):
        return self.__charge
    
    def charge(self):
        if self.__charge < 100:
            self.__charge += 1
        if self.__charge >= 100:
            self.__charge = 100
    