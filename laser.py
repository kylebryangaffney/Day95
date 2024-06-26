from turtle import Turtle

class Laser(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("square")
        self.color("red")
        self.shapesize(stretch_wid=1, stretch_len=0.2)
        self.penup()
        self.y_move = 10

    def travel(self):
        new_y = self.ycor() + self.y_move
        self.goto(self.xcor(), new_y)

    def shoot_down(self, shoot_down):
        if shoot_down:
            self.y_move = -10

