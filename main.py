# game.py
from turtle import Screen
from ship import Ship
from alien import Alien
from barrier import Barrier
from boss import Boss
from scoreboard import Scoreboard
from helpers import detect_hit, detect_boss_hit, determine_shooter, create_barriers, create_enemies
import time

# Initialize screen
screen = Screen()
screen.bgcolor("black")
screen.setup(width=800, height=600)
screen.title("Space Invasion")
screen.tracer(0)

scoreboard = Scoreboard()

enemies = []
create_enemies(enemies, 1)
barrier_list = []
create_barriers(barrier_list, 5)

ship = Ship()

# Key bindings
screen.listen()
screen.onkey(ship.go_left, "Left")
screen.onkeypress(ship.go_left, "Left")
screen.onkey(ship.go_right, "Right")
screen.onkeypress(ship.go_right, "Right")
screen.onkey(ship.shoot, "space")

is_running = True
boss_crashing = False  # Flag to indicate if the boss is crashing down
last_move_time = time.time()
last_shoot_time = time.time()  # Initial last shoot time
boss_shoot_time = time.time()
direction = 1  # 1 for right, -1 for left

move_rate = 0.4

boss = Boss()
boss_active = False

while is_running:
    current_time = time.time()
    if current_time - last_move_time > move_rate and not boss_crashing:
        edge_reached = False
        if enemies:
            for enemy in enemies:
                if enemy.ycor() < -225:
                    is_running = False
                    scoreboard.game_over()
                if (direction == 1 and enemy.xcor() > 275) or (direction == -1 and enemy.xcor() < -275):
                    edge_reached = True
                    break

            if edge_reached:
                direction *= -1
                for enemy in enemies:
                    enemy.move_alien("down")
            else:
                for enemy in enemies:
                    if direction == 1:
                        enemy.move_alien("right")  # Move right
                    else:
                        enemy.move_alien("left")  # Move left
        else:
            # All enemies are killed - activate the boss
            if not boss_active:
                boss_active = True
                boss.activate_boss()

        last_move_time = current_time

    if boss_active and not boss_crashing:
        # Move the boss at a faster rate
        if current_time - last_move_time > (move_rate / 50):
            if (direction == 1 and boss.xcor() > 275) or (direction == -1 and boss.xcor() < -275):
                direction *= -1
                boss.move_boss("down")
            else:
                if direction == 1:
                    boss.move_boss("right")
                else:
                    boss.move_boss("left")
            last_move_time = current_time

        # Boss shooting logic
        if current_time - boss_shoot_time > 2:
            boss.shoot()
            boss_shoot_time = current_time

    # Update the last_shoot_time by reference
    last_shoot_time = determine_shooter(enemies, current_time, last_shoot_time)

    time.sleep(0.05)

    if detect_hit(ship.lasers, enemies):
        enemies = [enemy for enemy in enemies if enemy.xcor() < 999]
        scoreboard.score_point()

    if detect_boss_hit(ship.lasers, boss, boss_active):
        if boss.health <= 0:
            boss.crash_down()
            boss_crashing = True  # Set the flag to indicate the boss is crashing

    if boss_crashing and boss.ycor() <= -225:
        is_running = False
        scoreboard.display_win()

    if detect_hit([laser for enemy in enemies for laser in enemy.lasers], [ship]) or detect_hit(boss.lasers, [ship]):
        scoreboard.lose_life()
        if scoreboard.lives == 0:
            is_running = False
            scoreboard.game_over()
        else:
            ship.goto(0, -275)

    if detect_hit(ship.lasers, barrier_list) or detect_hit([laser for enemy in enemies for laser in enemy.lasers], barrier_list) or detect_hit(boss.lasers, barrier_list):
        barrier_list = [barrier for barrier in barrier_list if barrier.xcor() < 999]

    screen.update()

screen.exitonclick()
