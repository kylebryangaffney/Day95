import turtle
from laser import Laser

MAX_LEFT = -350
MAX_RIGHT = 350
MAX_TOP = 250
MAX_BOTTOM = -250

alien_points = ((0, 0), (0, 10), (10, 10), (10, 20), (20, 20), (20, 10), (30, 10),
    (30, 0), (40, 0), (40, 10), (30, 10), (30, 20), (40, 20), (40, 30),
    (30, 30), (30, 40), (20, 40), (20, 30), (10, 30), (10, 40), (0, 40),
    (0, 30), (-10, 30), (-10, 20), (0, 20), (0, 10), (-10, 10), (-10, 0),
    (0, 0))

turtle.register_shape("alien", alien_points)

class Alien(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape("alien")
        self.color("white")
        self.shapesize(stretch_wid=0.5, stretch_len=0.5)
        self.left(90)
        self.penup()
        self.goto(0, 0)
        self.lasers = []

    def go_left(self):
        if self.xcor() > MAX_LEFT:
            new_x = self.xcor() - 20
            self.goto(new_x, self.ycor())

    def go_right(self):
        if self.xcor() < MAX_RIGHT:
            new_x = self.xcor() + 20
            self.goto(new_x, self.ycor())

    def go_up(self):
        if self.ycor() < MAX_TOP:
            new_y = self.ycor() + 20
            self.goto(self.xcor(), new_y)

    def go_down(self):
        if self.ycor() > MAX_BOTTOM:
            new_y = self.ycor() - 20
            self.goto(self.xcor(), new_y)

    def shoot(self):
        new_laser = Laser()
        new_laser.shoot_down(True)
        new_laser.penup()
        new_laser.goto(self.xcor() + 15, self.ycor() + 10)
        self.lasers.append(new_laser)
        self.move_laser(new_laser)

    def move_laser(self, laser):
        if laser.ycor() > -300: 
            laser.travel()
            turtle.ontimer(lambda: self.move_laser(laser), 10)
        else:
            laser.hideturtle()
            self.lasers.remove(laser)
