from random import randint


class ColorGenerator:
    def __init__(self):
        self.__generated_colors = []
    
    def generate_color(self):
        while True:
            r = randint(0, 255)
            g = randint(0, 255)
            b = randint(0, 255)
            color_obj = (r, g, b)
            if color_obj in self.__generated_colors:
                continue
            self.__generated_colors.append(color_obj)
            return color_obj
    
    def get_inactive_state_color(self):
        return (127, 127, 127)