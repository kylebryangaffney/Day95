# boss.py
import turtle
from laser import Laser

MAX_LEFT = -350
MAX_RIGHT = 350
MAX_TOP = 250
MAX_BOTTOM = -250

MOVE_INTERVAL = 3

# Define the boss mothership shape
boss_points = ((-20, 0), (-10, 0), (-10, -10), (0, -10), (0, 0),
    (10, 0), (10, -10), (20, -10), (20, 0), (30, 0),
    (30, -10), (40, -10), (40, 0), (50, 0), (50, -10),
    (60, -10), (60, 0), (70, 0), (70, -10), (80, -10),
    (80, 0), (90, 0), (90, -10), (100, -10), (100, 0),
    (110, 0), (110, -10), (120, -10), (120, 0), (130, 0),
    (130, 10), (120, 10), (120, 20), (110, 20), (110, 30),
    (100, 30), (100, 40), (90, 40), (90, 50), (80, 50),
    (80, 60), (70, 60), (70, 50), (60, 50), (60, 60),
    (50, 60), (50, 50), (40, 50), (40, 60), (30, 60),
    (30, 50), (20, 50), (20, 60), (10, 60), (10, 50),
    (0, 50), (0, 60), (-10, 60), (-10, 50), (-20, 50),
    (-20, 60), (-30, 60), (-30, 50), (-40, 50), (-40, 60),
    (-50, 60), (-50, 50), (-60, 50), (-60, 60), (-70, 60),
    (-70, 50), (-80, 50), (-80, 40), (-90, 40), (-90, 30),
    (-100, 30), (-100, 20), (-110, 20), (-110, 10), (-120, 10),
    (-120, 0), (-130, 0), (-130, -10), (-120, -10), (-120, 0),
    (-110, 0), (-110, -10), (-100, -10), (-100, 0), (-90, 0),
    (-90, -10), (-80, -10), (-80, 0), (-70, 0), (-70, -10),
    (-60, -10), (-60, 0), (-50, 0), (-50, -10), (-40, -10),
    (-40, 0), (-30, 0), (-30, -10), (-20, -10), (-20, 0))  # Close the shape

turtle.register_shape("boss", boss_points)

class Boss(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape("boss")
        self.color("yellow")
        self.shapesize(stretch_wid=0.66, stretch_len=0.66)
        self.left(90)
        self.penup()
        self.goto(0, 200)
        self.health = 12
        self.lasers = []

    def move_boss(self, direction):
        if direction == "down":
            self.go_down()
        elif direction == "left":
            self.go_left()
        elif direction == "right":
            self.go_right()

    def take_damage(self):
        self.health -= 1

    def activate_boss(self):
        self.color("red")

    def crash_down(self):
        if self.ycor() > MAX_BOTTOM:
            self.goto(self.xcor(), self.ycor() - MOVE_INTERVAL)
            turtle.ontimer(self.crash_down, 50)
        else:
            self.hideturtle()
            self.crashed = True  # Indicate that the boss has crashed

    def go_left(self):
        if self.xcor() > MAX_LEFT:
            new_x = self.xcor() - MOVE_INTERVAL
            self.goto(new_x, self.ycor())

    def go_right(self):
        if self.xcor() < MAX_RIGHT:
            new_x = self.xcor() + MOVE_INTERVAL
            self.goto(new_x, self.ycor())

    def go_up(self):
        if self.ycor() < MAX_TOP:
            new_y = self.ycor() + MOVE_INTERVAL
            self.goto(self.xcor(), new_y)

    def go_down(self):
        if self.ycor() > MAX_BOTTOM:
            new_y = self.ycor() - MOVE_INTERVAL
            self.goto(self.xcor(), new_y)

    def shoot(self):
        new_laser = Laser()
        new_laser.shoot_down(True)
        new_laser.penup()
        new_laser.goto(self.xcor(), self.ycor() - 20)
        self.lasers.append(new_laser)
        self.move_laser(new_laser)

    def move_laser(self, laser):
        if laser.ycor() > -300: 
            laser.travel()
            turtle.ontimer(lambda: self.move_laser(laser), 10)
        else:
            laser.hideturtle()
            self.lasers.remove(laser)
