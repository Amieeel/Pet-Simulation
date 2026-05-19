import pygame
from button import Button
pygame.init()

WIDTH, HEIGHT = 475, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Load Buttons
play_button = Button(160, 275, "images/PlayButton.png", 3)
bathroom_button = Button(421, 495, "images/BathroomButton.png", 1)
bedroom_button = Button(421, 470, "images/BedroomButton.png", 1)

game_state = "menu"

def Switch(game_state):
    if game_state == "menu":
        if play_button.draw(screen):  
            print("clicked")
            game_state = "bedroom" 

    elif game_state == "bedroom":
        if bathroom_button.draw(screen):
            game_state = "bathroom"

    elif game_state == "bathroom":
        if bedroom_button.draw(screen):
            game_state = "bedroom"

    return game_state