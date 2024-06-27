# main.py
# import turtle
from turtle import Screen
from ship import Ship
from alien import Alien
from barrier import Barrier
from scoreboard import Scoreboard
import random
import time

# Initialize screen
screen = Screen()
screen.bgcolor("black")
screen.setup(width=800, height=600)
screen.title("Space Invasion")
screen.tracer(0)

scoreboard = Scoreboard()

def detect_hit(lasers, targets):
    for laser in lasers:
        for target in targets:
            if abs(laser.xcor() - target.xcor()) < 20 and abs(laser.ycor() - target.ycor()) < 15:
                laser.hideturtle()
                lasers.remove(laser)
                target.goto(999, 999)
                return True
    return False

def determine_shooter(enemy_list):
    global last_shoot_time
    if not enemy_list:
        return

    shooting_interval = min(1.5, len(enemy_list) * 0.5)
    if current_time - last_shoot_time > shooting_interval:
        # Choose a random enemy with a slight preference for closer ones (optional)
        shooter_candidates = sorted(enemy_list, key=lambda enemy: abs(enemy.xcor()))
        shooter_enemy = random.choice(shooter_candidates)
        shooter_enemy.shoot()
        last_shoot_time = current_time

barrier_list = []

def create_barriers(amount):
    spacing = 700 // (amount - 1)
    start_x = -350
    for i in range(amount):
        barrier = Barrier()
        barrier.goto(start_x + i * spacing, -100)
        barrier_list.append(barrier)

create_barriers(5)

ship = Ship()
enemies = []
for i in range(15):
    new_x = -200 + (30 * i)
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

is_running = True
last_move_time = time.time()
last_shoot_time = time.time()
direction = 1  # 1 for right, -1 for left

while is_running:
    current_time = time.time()
    if current_time - last_move_time > 1:
        edge_reached = False
        for enemy in enemies:
            if (direction == 1 and enemy.xcor() > 350) or (direction == -1 and enemy.xcor() < -350):
                edge_reached = True
                break

        if edge_reached:
            direction *= -1
            for enemy in enemies:
                enemy.go_down()
        else:
            for enemy in enemies:
                if direction == 1:
                    enemy.go_right()
                else:
                    enemy.go_left()
                
        last_move_time = current_time

    determine_shooter(enemies)

    time.sleep(0.05)

    if detect_hit(ship.lasers, enemies):
        enemies = [enemy for enemy in enemies if enemy.xcor() < 999]
        scoreboard.score_point()

    if detect_hit([laser for enemy in enemies for laser in enemy.lasers], [ship]):
        scoreboard.lose_life()
        if scoreboard.lives == 0:
            is_running = False
            scoreboard.game_over()
        else:
            ship.goto(0, -275)

    if detect_hit(ship.lasers, barrier_list) or detect_hit([laser for enemy in enemies for laser in enemy.lasers], barrier_list):
        barrier_list = [barrier for barrier in barrier_list if barrier.xcor() < 999]

    screen.update()

screen.exitonclick()
