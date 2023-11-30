
class Location:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z
        self.obj_at_location = None
    def get_position(self):
        return (self.x, self.y)