import turtle
from laser import Laser

# Constants for the movement boundaries of the alien
MAX_LEFT = -350
MAX_RIGHT = 350
MAX_TOP = 250
MAX_BOTTOM = -250

# Interval for each move step
MOVE_INTERVAL = 6

# Points to define the shape of the alien
alien_points = (
    (0, 0), (0, 10), (10, 10), (10, 20), (20, 20), (20, 10), (30, 10),
    (30, 0), (40, 0), (40, 10), (30, 10), (30, 20), (40, 20), (40, 30),
    (30, 30), (30, 40), (20, 40), (20, 30), (10, 30), (10, 40), (0, 40),
    (0, 30), (-10, 30), (-10, 20), (0, 20), (0, 10), (-10, 10), (-10, 0),
    (0, 0)
)

# Register the shape with turtle graphics
turtle.register_shape("alien", alien_points)

class Alien(turtle.Turtle):
    """
    This class represents an alien in the Space Invasion game.

    Attributes:
        lasers (list): A list of lasers shot by the alien.
    """
    
    def __init__(self):
        """Initializes the alien with its shape, color, position, and direction."""
        super().__init__()
        self.shape("alien")
        self.color("white")
        self.shapesize(stretch_wid=0.5, stretch_len=0.5)
        self.left(90)
        self.penup()
        self.goto(0, 0)
        self.lasers = []

    def move_alien(self, direction):
        """
        Moves the alien in the specified direction.

        Args:
            direction (str): The direction to move the alien ('down', 'left', 'right').
        """
        if direction == "down":
            self.go_down()
        elif direction == "left":
            self.go_left()
        elif direction == "right":
            self.go_right()

    def go_left(self):
        """Moves the alien left by MOVE_INTERVAL units if within the left boundary."""
        if self.xcor() > MAX_LEFT:
            new_x = self.xcor() - MOVE_INTERVAL
            self.goto(new_x, self.ycor())

    def go_right(self):
        """Moves the alien right by MOVE_INTERVAL units if within the right boundary."""
        if self.xcor() < MAX_RIGHT:
            new_x = self.xcor() + MOVE_INTERVAL
            self.goto(new_x, self.ycor())

    def go_up(self):
        """Moves the alien up by MOVE_INTERVAL units if within the top boundary."""
        if self.ycor() < MAX_TOP:
            new_y = self.ycor() + MOVE_INTERVAL
            self.goto(self.xcor(), new_y)

    def go_down(self):
        """Moves the alien down by MOVE_INTERVAL units if within the bottom boundary."""
        if self.ycor() > MAX_BOTTOM:
            new_y = self.ycor() - MOVE_INTERVAL
            self.goto(self.xcor(), new_y)

    def shoot(self):
        """
        Shoots a laser from the alien's current position.
        """
        new_laser = Laser()
        new_laser.shoot_down(True)
        new_laser.penup()
        new_laser.goto(self.xcor() + 15, self.ycor() + 10)
        self.lasers.append(new_laser)
        self.move_laser(new_laser)

    def move_laser(self, laser):
        """
        Moves the laser down the screen. If the laser moves off the screen, it is removed.

        Args:
            laser (Laser): The laser to be moved.
        """
        if laser.ycor() > -300:
            laser.travel()
            turtle.ontimer(lambda: self.move_laser(laser), 10)
        else:
            laser.hideturtle()
            self.lasers.remove(laser)
