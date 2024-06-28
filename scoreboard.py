# scoreboard
from turtle import Turtle

class Scoreboard(Turtle):

    def __init__(self):
        super().__init__()
        self.color("white")
        self.penup()
        self.hideturtle()
        self.score = 0
        self.lives = 3
        self.goto(0, 250)
        self.update_score()

    def update_score(self):
        self.clear()
        self.write(f"Score: {self.score} Lives: {self.lives}", align="center", font=("Courier", 33, "normal"))

    def score_point(self):
        self.score += 1
        self.update_score()

    def reset(self):
        self.score = 0
        self.lives = 3
        self.update_score()

    def lose_life(self):
        if self.lives > 0:
            self.lives -= 1
        self.update_score()

    def game_over(self):
        self.goto(0, 0)
        self.write("GAME OVER", align="center", font=("Courier", 40, "normal"))
    
    def display_win(self):
        self.goto(0, 0)
        self.write("VICTORY", align="center", font=("Courier", 40, "normal"))
