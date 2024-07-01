from turtle import Turtle

class Scoreboard(Turtle):
    """
    This class represents the scoreboard in the Space Invasion game.

    Attributes:
        score (int): The current score of the player.
        lives (int): The number of lives the player has remaining.
    """

    def __init__(self):
        """Initializes the scoreboard with default score and lives, and sets up its appearance."""
        super().__init__()
        self.color("white")
        self.penup()
        self.hideturtle()
        self.score = 0
        self.lives = 3
        self.goto(0, 250)
        self.update_score()

    def update_score(self):
        """Clears the previous score display and updates it with the current score and lives."""
        self.clear()
        self.write(f"Score: {self.score} Lives: {self.lives}", align="center", font=("Courier", 33, "normal"))

    def score_point(self):
        """Increments the score by one and updates the scoreboard."""
        self.score += 1
        self.update_score()

    def reset(self):
        """Resets the score and lives to their default values and updates the scoreboard."""
        self.score = 0
        self.lives = 3
        self.update_score()

    def lose_life(self):
        """Decrements the lives by one (if greater than zero) and updates the scoreboard."""
        if self.lives > 0:
            self.lives -= 1
        self.update_score()

    def game_over(self):
        """Displays the 'GAME OVER' message at the center of the screen."""
        self.goto(0, 0)
        self.write("GAME OVER", align="center", font=("Courier", 40, "normal"))
    
    def display_win(self):
        """Displays the 'VICTORY' message at the center of the screen."""
        self.goto(0, 0)
        self.write("VICTORY", align="center", font=("Courier", 40, "normal"))
