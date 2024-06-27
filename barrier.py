from turtle import Turtle


class Barrier(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("square")
        self.color("white")
        self.shapesize(stretch_wid=0.66, stretch_len=1.66)
        self.penup()

    
