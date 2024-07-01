from turtle import Turtle

class Barrier(Turtle):
    """
    This class represents a barrier in the Space Invasion game.

    Attributes:
        health (int): The current health of the barrier.
        health_colors (list): A list of colors representing the barrier's health states.
    """

    def __init__(self):
        """Initializes the barrier with its shape, color, position, and health."""
        super().__init__()
        self.shape("square")
        self.health = 3
        self.health_colors = ["maroon", "orange", "yellow"]
        self.color(self.health_colors[self.health - 1])
        self.shapesize(stretch_wid=0.66, stretch_len=1.66)
        self.penup()

    def take_damage(self):
        """Reduces the barrier's health by one and updates its color. Destroys the barrier if health is zero."""
        self.health -= 1
        if self.health > 0:
            self.color(self.health_colors[self.health - 1])
        else:
            self.destroy_barrier()

    def destroy_barrier(self):
        """Moves the barrier off-screen to simulate its destruction."""
        self.goto(999, 999)
