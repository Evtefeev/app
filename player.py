from dataclasses import dataclass
from turtle import Turtle


@dataclass
class Player:
    x: int
    y: int
    shape: str
    color: str
    penup: bool
    turtle: Turtle

    def goto(self, x, y):
        self.x = x
        self.y = y

    def xcor(self):
        return self.x

    def ycor(self):
        return self.y

    def update(self):
        # Create a new turtle for new players
        if not self.turtle:
            self.turtle = Turtle()
        self.turtle.shape(self.shape)
        self.turtle.color(self.color)
        if self.penup:
            self.turtle.penup()
        else:
            self.turtle.pendown()
        self.turtle.goto(self.x, self.y)
