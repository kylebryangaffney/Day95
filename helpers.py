# helpers.py
import random
from ship import Ship
from alien import Alien
from barrier import Barrier
from boss import Boss
from scoreboard import Scoreboard

def detect_hit(lasers, targets):
    for laser in lasers:
        for target in targets:
            if abs(laser.xcor() - target.xcor()) < 20 and abs(laser.ycor() - target.ycor()) < 15:
                laser.hideturtle()
                lasers.remove(laser)
                target.goto(999, 999)
                return True
    return False

def detect_boss_hit(lasers, boss, boss_active):
    if boss_active:
        for laser in lasers:
            if abs(laser.xcor() - boss.xcor()) < 20 and abs(laser.ycor() - boss.ycor()) < 15:
                laser.hideturtle()
                lasers.remove(laser)
                boss.take_damage()
                return True
    return False

def determine_shooter(enemy_list, current_time, last_shoot_time):
    if not enemy_list:
        return last_shoot_time  # Return the last shoot time

    shooting_interval = min(1.5, len(enemy_list) * 0.5)
    if current_time - last_shoot_time > shooting_interval:
        # Choose a random enemy with a preference for closer ones
        shooter_candidates = sorted(enemy_list, key=lambda enemy: abs(enemy.xcor()))
        shooter_enemy = random.choice(shooter_candidates)
        shooter_enemy.shoot()
        last_shoot_time = current_time
    
    return last_shoot_time  # Return the updated last shoot time

def create_barriers(barrier_list, amount):
    spacing = 700 // (amount - 1)
    start_x = -350
    for i in range(amount):
        barrier = Barrier()
        barrier.goto(start_x + i * spacing, -100)
        barrier_list.append(barrier)

def create_enemies(enemy_list, rows):
    for row in range(rows):
        for i in range(13):
            new_x = -300 + (45 * i)
            new_y = 50 - (30 * row)
            new_alien = Alien()
            new_alien.goto(new_x, new_y)
            enemy_list.append(new_alien)
