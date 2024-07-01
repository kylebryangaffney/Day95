from turtle import Turtle

class Laser(Turtle):
    """
    This class represents a laser shot in the Space Invasion game.

    Attributes:
        y_move (int): The vertical movement increment for the laser.
    """
    
    def __init__(self):
        """Initializes the laser with its shape, color, size, and position."""
        super().__init__()
        self.shape("square")
        self.color("green")
        self.shapesize(stretch_wid=1, stretch_len=0.2)
        self.penup()
        self.y_move = 10

    def travel(self):
        """Moves the laser upwards by its y_move attribute."""
        new_y = self.ycor() + self.y_move
        self.goto(self.xcor(), new_y)

    def shoot_down(self, shoot_down):
        """
        Sets the laser's direction to downwards if shoot_down is True.

        Args:
            shoot_down (bool): If True, sets the laser to move downwards.
        """
        if shoot_down:
            self.y_move = -10
