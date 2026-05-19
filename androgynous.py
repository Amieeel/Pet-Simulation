import random
import time
from player import Player
from mood import HappyMood, AngryMood, BoredMood, NeutralMood, SadMood
from database import create_connection

class Androgynous(Player):
    def __init__(self):
        self._age = 0
        self._energy = 100
        self._health = 100
        self._hunger = 100
        self._mood = 100
        self._hygiene = 100
        self.likes = []
        self.dislikes = []
        self.moving = False
        self.time_passed = 0

        # Frame indexes
        self.sleep_level = 0
        self.potty_level = 0
        self.shower_level = 0
        self.hunger_level = 0

        # Timers
        self.sleep_timer = time.time()
        self.potty_timer = time.time()
        self.shower_timer = time.time()
        self.hunger_timer = time.time()

        # Frame delays (seconds per frame)
        self.sleep_delay = 30  # 30 seconds
        self.potty_delay = 40  # 40 seconds
        self.shower_delay = 60  # 1 minute
        self.hunger_delay = 30  # 30 seconds

        self.name = "Ziddy"  # Ensure name exists

    def save_to_db(self):
        conn = create_connection()
        c = conn.cursor()
        c.execute("DELETE FROM player_data")  # Single save slot
        c.execute('''
            INSERT INTO player_data (name, hunger_level, sleep_level, shower_level, potty_level, mood, age)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            self.name,
            self.hunger_level,
            self.shower_level,     # Cleanliness mapped to shower_level
            self.sleep_level,      # Energy mapped to sleep_level
            self.potty_level,      # Poop status
            self._mood,
            self._age
        ))
        conn.commit()
        conn.close()

    def load_from_db(self):
        conn = create_connection()
        c = conn.cursor()
        c.execute("SELECT name, hunger_level, shower_level, sleep_level, potty_level, mood, age FROM player_data LIMIT 1")
        row = c.fetchone()
        conn.close()

        if row:
            self.name = row[0]
            self.hunger_level = row[1]
            self.shower_level = row[2]
            self.sleep_level = row[3]
            self.potty_level = row[4]
            self._mood = row[5]
            self._age = row[6]


    @property
    def age(self): return self._age
    @property
    def energy(self): return self._energy
    @property
    def health(self): return self._health
    @property
    def hunger(self): return self._hunger
    @property
    def mood(self): return self._mood
    @property
    def potty(self): return self._hygiene

    def player_eats(self, food):
        if food not in self.dislikes:
            self._energy += 5
            self._hunger += 30
            self.hunger_level = max(0, self.hunger_level - 1)
        else:
            self._health -= 15

    def player_moves(self):
        if self.moving:
            self._energy -= 5
            self.moving = False

    def player_plays(self):
        self._energy -= 20

    def player_sleeps(self):
        self._age += 1
        self._energy += 10
        self.sleep_level = max(0, self.sleep_level - 1)

    def player_poops(self):
        if self._hygiene <= 25:
            print("Need potty!")
        self._hygiene -= 25
        self.potty_level = max(0, self.potty_level - 1)

    def player_showers(self):
        self._hygiene += 30
        self.shower_level = max(0, self.shower_level - 1)

    def health_check(self):
        if self._hunger < 75:
            self.player_moves()
        if self._hunger < 1:
            self.game_over()

def __init__(self):
    self.mood = NeutralMood()
    self.last_mood_sound_time = 0

    def update_mood(self):
        if 75 <= self._mood <= 100:
            self.mood = HappyMood()
        elif 50 <= self._mood <= 74:
            self.mood = NeutralMood()
        elif 30 <= self._mood <= 49:
            self.mood = BoredMood()
        elif 10 <= self._mood <= 29:
            self.mood = SadMood()
        elif 1 <= self._mood <= 9:
            self.mood = AngryMood()

    def game_over(self):
        print("Game Over! Your health reached 0.")
        exit()

    def random_move(self):
        self.moving = random.choice([True, False])
        if self.moving:
            print("Moving...")
        self.player_moves()
