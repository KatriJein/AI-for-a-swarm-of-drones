
from Drone_State import DroneState

class ChargingState(DroneState):
    def __init__(self, taken_energy=0):
        super().__init__(taken_energy)

    def act(self, drone):
        # drone.charge()
        st = drone.get_station()
        st.charge_drone(drone)
        if drone.is_full_energy():
            st.remove_drone(drone)
            #drone.wait()
            