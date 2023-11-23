import turtle

WIDTH, HEIGHT = 1000, 700

screen = turtle.Screen()
screen.setup(WIDTH, HEIGHT)
screen.setworldcoordinates(0, 0, WIDTH, HEIGHT)
screen.bgpic("fone.gif")
screen.cv._rootwindow.resizable(False, False)

turtle.mainloop()