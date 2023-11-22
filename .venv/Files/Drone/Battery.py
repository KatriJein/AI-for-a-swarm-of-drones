
USUAL_CHARGE = 100
LOW_LEVEL_SIDE = 20

class Battery:
    def __init__(self, charge=USUAL_CHARGE):
        self.__charge = charge

    def take_energy(self, amount):
        self.__charge -= amount

    def is_low(self):
        return self.__charge < LOW_LEVEL_SIDE
    