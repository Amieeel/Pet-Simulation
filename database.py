import sqlite3

DB_NAME = "playerdata.db"

def create_connection():
    return sqlite3.connect("playerdata.db")

# --- Create table if it doesn't exist ---
def create_table():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS player_data (
            id INTEGER PRIMARY KEY,
            name TEXT,
            sleep_level INTEGER,
            hunger_level INTEGER,
            shower_level INTEGER,
            potty_level INTEGER,
            mood INTEGER,
            age INTEGER,
            alive INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def force_reset_table():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS player_data")  # Deletes old broken table
    conn.commit()
    conn.close()
    create_table()  # Recreate the table with correct schema

# --- Save player data ---
def save_player(player):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("DELETE FROM player")  # Only one save slot
    c.execute('''
        INSERT INTO player (
            name, sleep_level, hunger_level, shower_level, potty_level,
            mood, sleep_level, age, alive
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        player.name, player.energy, player.hunger, player.cleanliness,
        player.poop_level, player.mood, player.sleep_level,
        player.age, int(player.alive)
    ))

    conn.commit()
    conn.close()

# --- Load player data ---
def load_player(player):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM player LIMIT 1")
    row = c.fetchone()
    conn.close()

    if row:
        (_, name, energy, hunger, cleanliness, poop, mood,
         sleep, age, alive) = row
        player.name = name
        player.energy = energy
        player.hunger = hunger
        player.cleanliness = cleanliness
        player.poop_level = poop
        player.mood = mood
        player.sleep_level = sleep
        player.age = age
        player.alive = bool(alive)
        return True
    return False

# --- Check if player is dead (for auto-restart prevention) ---
def is_player_dead():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT alive FROM player LIMIT 1")
    row = c.fetchone()
    conn.close()
    return row and row[0] == 0
