import random
from ship import Ship
from alien import Alien
from barrier import Barrier
from boss import Boss
from scoreboard import Scoreboard

def detect_barrier_hits(lasers, barriers):
    """
    Detects collisions between lasers and barriers.

    Args:
        lasers (list): A list of laser objects.
        barriers (list): A list of barrier objects.

    Returns:
        list: A list of tuples where each tuple contains a laser and a barrier that collided.
    """
    hits = []
    for laser in lasers:
        for barrier in barriers:
            if abs(laser.xcor() - barrier.xcor()) < 20 and abs(laser.ycor() - barrier.ycor()) < 15:
                hits.append((laser, barrier))
    return hits

def detect_hit(lasers, targets):
    """
    Detects collisions between lasers and targets (e.g., enemies, ship).

    Args:
        lasers (list): A list of laser objects.
        targets (list): A list of target objects.

    Returns:
        bool: True if a hit is detected, False otherwise.
    """
    for laser in lasers:
        for target in targets:
            if abs(laser.xcor() - target.xcor()) < 20 and abs(laser.ycor() - target.ycor()) < 15:
                laser.hideturtle()
                lasers.remove(laser)
                target.goto(999, 999)  # Move the target off-screen
                return True
    return False

def detect_boss_hit(lasers, boss, boss_active):
    """
    Detects collisions between lasers and the boss.

    Args:
        lasers (list): A list of laser objects.
        boss (Boss): The boss object.
        boss_active (bool): True if the boss is active, False otherwise.

    Returns:
        bool: True if a hit is detected, False otherwise.
    """
    if boss_active:
        for laser in lasers:
            if abs(laser.xcor() - boss.xcor()) < 20 and abs(laser.ycor() - boss.ycor()) < 15:
                laser.hideturtle()
                lasers.remove(laser)
                boss.take_damage()
                return True
    return False

def determine_shooter(enemy_list, current_time, last_shoot_time):
    """
    Determines which enemy will shoot next based on the current time and the last shoot time.

    Args:
        enemy_list (list): A list of enemy objects.
        current_time (float): The current time.
        last_shoot_time (float): The last time an enemy shot.

    Returns:
        float: The updated last shoot time.
    """
    if not enemy_list:
        return last_shoot_time  # Return the last shoot time

    shooting_interval = min(1.5, len(enemy_list) * 0.5)
    if current_time - last_shoot_time > shooting_interval:
        # Choose an enemy with a preference for closer ones
        shooter_candidates = sorted(enemy_list, key=lambda enemy: abs(enemy.xcor()))
        shooter_enemy = random.choice(shooter_candidates)
        shooter_enemy.shoot()
        last_shoot_time = current_time
    
    return last_shoot_time  # Return the updated last shoot time

def create_barriers(barrier_list, amount):
    """
    Creates a specified number of barriers and adds them to the barrier list.

    Args:
        barrier_list (list): The list to store the created barrier objects.
        amount (int): The number of barriers to create.
    """
    spacing = 700 // (amount - 1)
    start_x = -350
    for i in range(amount):
        barrier = Barrier()
        barrier.goto(start_x + i * spacing, -100)
        barrier_list.append(barrier)

def create_enemies(enemies, difficulty):
    """
    Creates a grid of enemies based on the difficulty level and adds them to the enemy list.

    Args:
        enemies (list): The list to store the created enemy objects.
        difficulty (int): The difficulty level, determining the number of rows of enemies.
    """
    rows = difficulty  # Number of rows is based on the difficulty
    columns = 10  # You can adjust the number of columns as needed
    x_start = -225
    y_start = 150
    x_offset = 50
    y_offset = 50

    for row in range(rows):
        for column in range(columns):
            enemy = Alien()
            enemy.goto(x_start + column * x_offset, y_start - row * y_offset)
            enemies.append(enemy)
