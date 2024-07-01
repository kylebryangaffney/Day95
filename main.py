from turtle import Screen
from ship import Ship
from alien import Alien
from barrier import Barrier
from boss import Boss
from scoreboard import Scoreboard
from helpers import detect_hit, detect_boss_hit, determine_shooter, create_barriers, create_enemies, detect_barrier_hits
import time

class SpaceInvasionGame:
    """
    This class represents the Space Invasion game.

    Attributes:
        difficulty (int): The difficulty level of the game.
        screen (Screen): The game screen.
        scoreboard (Scoreboard): The scoreboard of the game.
        ship (Ship): The player's ship.
        enemies (list): A list of enemy Alien objects.
        barriers (list): A list of Barrier objects.
        boss (Boss): The boss enemy.
        boss_active (bool): Indicates if the boss is active.
        boss_crashing (bool): Indicates if the boss is crashing.
        last_move_time (float): The last time enemies moved.
        last_shoot_time (float): The last time an enemy shot.
        boss_shoot_time (float): The last time the boss shot.
        direction (int): The current direction of enemies' movement (1 for right, -1 for left).
        move_rate (float): The rate at which enemies move.
        is_running (bool): Indicates if the game is running.
    """
    
    def __init__(self, difficulty=1):
        """
        Initializes the SpaceInvasionGame with a specified difficulty level.

        Args:
            difficulty (int): The difficulty level of the game (default is 1).
        """
        self.screen = Screen()
        self.screen.bgcolor("black")
        self.screen.setup(width=800, height=600)
        self.screen.title("Space Invasion 666")
        self.screen.tracer(0)
        self.difficulty = difficulty

        self.scoreboard = Scoreboard()
        self.ship = Ship()
        self.ship.set_fire_delay(self.difficulty)  # Set the fire delay based on difficulty
        self.enemies = []
        create_enemies(self.enemies, self.difficulty)
        self.barriers = []
        create_barriers(self.barriers, 10)
        
        self.boss = Boss()
        self.boss_active = False
        self.boss_crashing = False

        self.last_move_time = time.time()
        self.last_shoot_time = time.time()
        self.boss_shoot_time = time.time()

        self.direction = 1  # 1 for right, -1 for left
        self.move_rate = 0.4
        self.is_running = True

        self.setup_key_bindings()

    def setup_key_bindings(self):
        """Sets up key bindings for controlling the ship."""
        self.screen.listen()
        self.screen.onkey(self.ship.go_left, "Left")
        self.screen.onkeypress(self.ship.go_left, "Left")
        self.screen.onkey(self.ship.go_right, "Right")
        self.screen.onkeypress(self.ship.go_right, "Right")
        self.screen.onkey(self.ship.shoot, "space")

    def move_enemies(self):
        """
        Moves all enemies in the current direction. If any enemy reaches the edge of the screen, all enemies move down and change direction.
        """
        edge_reached = False
        for enemy in self.enemies:
            if enemy.ycor() < -225:
                self.is_running = False
                self.scoreboard.game_over()
            if (self.direction == 1 and enemy.xcor() > 275) or (self.direction == -1 and enemy.xcor() < -275):
                edge_reached = True
                break

        if edge_reached:
            self.direction *= -1
            for enemy in self.enemies:
                enemy.move_alien("down")
        else:
            for enemy in self.enemies:
                if self.direction == 1:
                    enemy.move_alien("right")  # Move right
                else:
                    enemy.move_alien("left")  # Move left

    def move_boss(self):
        """
        Moves the boss in the current direction. If the boss reaches the edge of the screen, it moves down and changes direction.
        """
        if (self.direction == 1 and self.boss.xcor() > 275) or (self.direction == -1 and self.boss.xcor() < -275):
            self.direction *= -1
            self.boss.move_boss("down")
        else:
            if self.direction == 1:
                self.boss.move_boss("right")
            else:
                self.boss.move_boss("left")

    def update(self):
        """
        Updates the game state, including moving enemies, handling collisions, and updating the scoreboard.
        """
        current_time = time.time()
        
        if current_time - self.last_move_time > self.move_rate and not self.boss_crashing:
            if self.enemies:
                self.move_enemies()
            else:
                if not self.boss_active:
                    self.boss_active = True
                    self.boss.activate_boss()
            self.last_move_time = current_time

        if self.boss_active and not self.boss_crashing:
            if current_time - self.last_move_time > (self.move_rate / 50):
                self.move_boss()
                self.last_move_time = current_time

            if current_time - self.boss_shoot_time > 2:
                self.boss.shoot()
                self.boss_shoot_time = current_time

        self.last_shoot_time = determine_shooter(self.enemies, current_time, self.last_shoot_time)

        time.sleep(0.05)

        if detect_hit(self.ship.lasers, self.enemies):
            self.enemies = [enemy for enemy in self.enemies if enemy.xcor() < 999]
            self.scoreboard.score_point()

        if detect_boss_hit(self.ship.lasers, self.boss, self.boss_active):
            if self.boss.health <= 0:
                self.boss.crash_down()
                self.boss_crashing = True

        if self.boss_crashing and self.boss.ycor() <= -225:
            self.is_running = False
            self.scoreboard.display_win()

        if detect_hit([laser for enemy in self.enemies for laser in enemy.lasers], [self.ship]) or detect_hit(self.boss.lasers, [self.ship]):
            self.scoreboard.lose_life()
            if self.scoreboard.lives == 0:
                self.is_running = False
                self.scoreboard.game_over()
            else:
                self.ship.goto(0, -275)

        # Handle hits on barriers by ship lasers
        ship_laser_hits = detect_barrier_hits(self.ship.lasers, self.barriers)
        for laser, barrier in ship_laser_hits:
            laser.hideturtle()
            self.ship.lasers.remove(laser)
            if barrier.xcor() < 999:
                barrier.take_damage()

        # Handle hits on barriers by enemy lasers
        enemy_laser_hits = detect_barrier_hits([laser for enemy in self.enemies for laser in enemy.lasers], self.barriers)
        for laser, barrier in enemy_laser_hits:
            laser.hideturtle()
            for enemy in self.enemies:
                if laser in enemy.lasers:
                    enemy.lasers.remove(laser)
                    break
            if barrier.xcor() < 999:
                barrier.take_damage()

        # Handle hits on barriers by boss lasers
        boss_laser_hits = detect_barrier_hits(self.boss.lasers, self.barriers)
        for laser, barrier in boss_laser_hits:
            laser.hideturtle()
            self.boss.lasers.remove(laser)
            if barrier.xcor() < 999:
                barrier.take_damage()

        self.barriers = [barrier for barrier in self.barriers if barrier.xcor() < 999]

        self.screen.update()

    def run(self):
        """
        Runs the main game loop until the game is no longer running.
        """
        while self.is_running:
            self.update()
        self.screen.exitonclick()

if __name__ == "__main__":
    difficulty = 3
    game = SpaceInvasionGame(difficulty)
    game.run()
