# ship.py
import turtle
from laser import Laser

MAX_LEFT = -350
MAX_RIGHT = 350
MAX_TOP = 250
MAX_BOTTOM = -250

ship_points = ((0, 0), (10, 0), (10, -10), (20, -10), (20, 0), (30, 0), (30, -10),
    (40, -10), (40, 0), (50, 0), (50, 10), (40, 10), (40, 20), (30, 20),
    (30, 30), (20, 30), (20, 40), (10, 40), (10, 30), (0, 30), (0, 20),
    (-10, 20), (-10, 10), (-20, 10), (-20, 0), (-10, 0), (-10, -10),
    (0, -10), (0, 0))

turtle.register_shape("ship", ship_points)

class Ship(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape("ship")
        self.color("green")
        self.left(90)
        self.penup()
        self.goto(0, -275)
        self.lasers = []

    def go_left(self):
        if self.xcor() > MAX_LEFT:
            new_x = self.xcor() - 10
            self.goto(new_x, self.ycor())

    def go_right(self):
        if self.xcor() < MAX_RIGHT:
            new_x = self.xcor() + 10
            self.goto(new_x, self.ycor())

    def shoot(self):
        new_laser = Laser()
        new_laser.penup()
        new_laser.goto(self.xcor() + 15, self.ycor() + 10)
        self.lasers.append(new_laser)
        self.move_laser(new_laser)

    def move_laser(self, laser):
        if laser.ycor() < 300: 
            laser.travel()
            turtle.ontimer(lambda: self.move_laser(laser), 10)
        else:
            laser.hideturtle()
            self.lasers.remove(laser)