import pygame

pygame.mixer.init()

# Helper to load sound effects
def load_sound(filename, volume=0.5):
    sound = pygame.mixer.Sound(f"sounds/{filename}")
    sound.set_volume(volume)
    return sound

# === RANDOM SOUNDS ===
laughing = load_sound("laughing.wav", 0.7)
laughing_2 = load_sound("laughing_2.wav", 0.7)

# === EMOTION SOUNDS ===
angry = load_sound("angry.wav", 0.3)
bored = load_sound("bored.wav", 0.3)
happy = load_sound("happy.wav", 0.3)
neutral = load_sound("neutral.wav", 0.3)
sad = load_sound("sad.wav", 0.3)

# === ACTION SOUNDS ===
drinking = load_sound("drinking.wav", 0.6)
eating = load_sound("eating.wav", 0.6)
pooping = load_sound("pooping.wav", 0.6)
sleeping = load_sound("sleeping.wav", 0.4)
showering = load_sound("shower.wav", 0.3)
humming = load_sound("humming.wav", 0.4)

# === UI / ENVIRONMENT SOUNDS ===
select_sound = load_sound("select_sound.wav", 0.5)
death = load_sound("death.wav", 0.3)

# === BACKGROUND MUSIC ===
def play_bgm():
    pygame.mixer.music.load("sounds/bgm.wav")
    pygame.mixer.music.set_volume(0.2)  # Adjust volume as needed
    pygame.mixer.music.play(-1)         # Loop indefinitely

def play_death_music():
    pygame.mixer.music.load("sounds/game_over_sound.wav")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)

def stop_bgm():
    pygame.mixer.music.stop()

