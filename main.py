import turtle
from turtle import Screen
from ship import Ship
from alien import Alien
from barrier import Barrier

import time

# Initialize screen
screen = Screen()
screen.bgcolor("black")
screen.setup(width=800, height=600)
screen.title("Space Invasion")
screen.tracer(0)

def detect_hit(lasers, targets):
    for laser in lasers:
        for target in targets:
            if abs(laser.xcor() - target.xcor()) < 20 and abs(laser.ycor() - target.ycor()) < 15:
                laser.hideturtle()
                lasers.remove(laser)
                target.goto(999, 999)
                return True
    return False

barrier_list = []

def create_barriers():
    for x in range(-350, 351, 100):
        barrier = Barrier()
        barrier.goto(x, -100)
        barrier_list.append(barrier)

create_barriers()

ship = Ship()
enemies = []
for i in range(6):
    new_x = -200 + (70 * i)
    new_alien = Alien()
    new_alien.goto(new_x, 0)
    enemies.append(new_alien)

# Key bindings
screen.listen()
screen.onkey(ship.go_left, "Left")
screen.onkeypress(ship.go_left, "Left")
screen.onkey(ship.go_right, "Right")
screen.onkeypress(ship.go_right, "Right")
screen.onkey(ship.shoot, "space")

screen.onkey(enemies[2].shoot, "x")

is_running = True
while is_running:
    time.sleep(0.05)
    if detect_hit(ship.lasers, enemies):
        enemies = [enemy for enemy in enemies if enemy.xcor() < 999]

    if detect_hit([laser for enemy in enemies for laser in enemy.lasers], [ship]):
        is_running = False
        print("Game Over!")

    if detect_hit(ship.lasers, barrier_list) or detect_hit([laser for enemy in enemies for laser in enemy.lasers], barrier_list):
        barrier_list = [barrier for barrier in barrier_list if barrier.xcor() < 999]

    screen.update()

screen.exitonclick()
