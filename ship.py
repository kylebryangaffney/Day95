import turtle
import time
from laser import Laser

# Constants for the movement boundaries of the ship
MAX_LEFT = -350
MAX_RIGHT = 350
MAX_TOP = 250
MAX_BOTTOM = -250

# Points to define the shape of the ship
ship_points = (
    (0, 0), (10, 0), (10, -10), (20, -10), (20, 0), (30, 0), (30, -10),
    (40, -10), (40, 0), (50, 0), (50, 10), (40, 10), (40, 20), (30, 20),
    (30, 30), (20, 30), (20, 40), (10, 40), (10, 30), (0, 30), (0, 20),
    (-10, 20), (-10, 10), (-20, 10), (-20, 0), (-10, 0), (-10, -10),
    (0, -10), (0, 0)
)

# Register the shape with turtle graphics
turtle.register_shape("ship", ship_points)

class Ship(turtle.Turtle):
    """
    This class represents the player's ship in the Space Invasion game.

    Attributes:
        lasers (list): A list of lasers shot by the ship.
        fire_delay (float): The delay between consecutive shots.
        last_shot_time (float): The last time the ship fired a laser.
    """

    def __init__(self):
        """Initializes the ship with its shape, color, position, and other attributes."""
        super().__init__()
        self.shape("ship")
        self.color("blue")
        self.left(90)
        self.penup()
        self.goto(0, -275)
        self.lasers = []
        self.fire_delay = 0
        self.last_shot_time = 0  # Track the last time the ship shot

    def go_left(self):
        """Moves the ship left by 10 units if within the left boundary."""
        if self.xcor() > MAX_LEFT:
            new_x = self.xcor() - 10
            self.goto(new_x, self.ycor())

    def set_fire_delay(self, difficulty):
        """
        Sets the fire delay based on the difficulty level.

        Args:
            difficulty (int): The difficulty level of the game.
        """
        self.fire_delay = 0.15 * difficulty  # Adjust the multiplier as needed

    def go_right(self):
        """Moves the ship right by 10 units if within the right boundary."""
        if self.xcor() < MAX_RIGHT:
            new_x = self.xcor() + 10
            self.goto(new_x, self.ycor())

    def shoot(self):
        """
        Shoots a laser if the fire delay time has passed since the last shot.
        """
        current_time = time.time()
        if current_time - self.last_shot_time >= self.fire_delay:
            new_laser = Laser()
            new_laser.penup()
            new_laser.goto(self.xcor() + 15, self.ycor() + 12)
            self.lasers.append(new_laser)
            self.move_laser(new_laser)
            self.last_shot_time = current_time  # Update the last shot time

    def move_laser(self, laser):
        """
        Moves the laser upwards. If the laser moves off the screen, it is removed.

        Args:
            laser (Laser): The laser to be moved.
        """
        if laser.ycor() < 300:
            laser.travel()
            turtle.ontimer(lambda: self.move_laser(laser), 15)
        else:
            laser.hideturtle()
            self.lasers.remove(laser)
