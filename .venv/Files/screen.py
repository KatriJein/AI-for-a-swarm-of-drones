import turtle
from Shared_constants import WIDTH, HEIGHT

class Background:
    def __init__(self, screen):
        screen.bgcolor("#d8ffc8")

if __name__ == "__main__":

    screen = turtle.Screen()
    screen.setup(WIDTH, HEIGHT)
    screen.setworldcoordinates(0, 0, WIDTH, HEIGHT)
    screen.cv._rootwindow.resizable(False, False)
    background = Background(screen)
    turtle.mainloop()