import pygame
import time
from button import Button
from androgynous import Androgynous
import sound
from sound import select_sound, death, play_death_music, stop_bgm, play_bgm
from database import create_table, create_connection, force_reset_table


create_table()
androgynous_player = Androgynous()
androgynous_player.load_from_db()
pygame.init()
sound.play_bgm()

# Screen setup
WIDTH, HEIGHT = 475, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Who's Your Ziddy?")

# Font
CutePixel = pygame.font.Font("CutePixel.ttf", 30)  # 30 is the font size

# Load images
home_TEXT = pygame.image.load('images/TitleText.png').convert_alpha()
titlescreen = pygame.image.load('images/TitleBG.png').convert_alpha()
bedroom = pygame.image.load('images/BedroomBG.png').convert_alpha()
bathroom = pygame.image.load('images/BathroomBG.png').convert_alpha()
arcade = pygame.image.load('images/ArcadeBG.png').convert_alpha()
kitchen = pygame.image.load('images/KitchenBG.png').convert_alpha()
gameoverBG = pygame.image.load('images/GameoverBG.png').convert_alpha()

food_menu = pygame.image.load('actions/Food_Menu.png').convert_alpha()
menu = pygame.image.load('images/menu_frame.png').convert_alpha()
LowOpac = pygame.image.load('images/settings/LowOpac.png').convert_alpha()
SettingsMenu = pygame.image.load('images/settings/SettingsMenu.png').convert_alpha()
reset_ques = pygame.image.load('images/settings/ResetQues.png').convert_alpha()


# Animation frames
sleep_stat = [pygame.image.load(f"Animation/Stats/Sleep/sleep{i}.png").convert_alpha() for i in range(11)]
toilet_stat = [pygame.image.load(f"Animation/Stats/Toilet/Bathroom{i}.png").convert_alpha() for i in range(11)]
shower_stat = [pygame.image.load(f"Animation/Stats/Shower/shower{i}.png").convert_alpha() for i in range(11)]
hunger_stat = [pygame.image.load(f"Animation/Stats/Hunger/hunger{i}.png").convert_alpha() for i in range(11)]

arcade_frames = [pygame.image.load(f"Animation/Arcade/frame{i}.png").convert_alpha() for i in range(17)]
shower_frames = [pygame.image.load(f"Animation/Bathroom/shower/shower{i}.png").convert_alpha() for i in range(15)]
bed_frames = [pygame.image.load(f"Animation/Bedroom/Bed{i}.png").convert_alpha() for i in range(4)]

# Player Animations
player_animation = [pygame.image.load(f"Animation/Player/Player{i}.png").convert_alpha() for i in range(4)]
diddy_stat = [pygame.image.load(f"Animation/Diddy/Diddy{i}.png").convert_alpha() for i in range(5)]
player_back = pygame.image.load("images/PlayerBackview.png").convert_alpha()
player_sleep = [pygame.image.load(f"Animation/Bedroom/Sleeping/sleep{i}.png").convert_alpha() for i in range(13)]
player_eat = [pygame.image.load(f"Animation/Eating/eat{i}.png").convert_alpha() for i in range(13)]
player_poop = [pygame.image.load(f"Animation/Bathroom/potty/toilet{i}.png").convert_alpha() for i in range(13)]
player_death = [pygame.image.load(f"Animation/Player/dying/d{i}.png").convert_alpha() for i in range(17)]

# Buttons
play_button = Button(160, 275, "images/PlayButton.png", 4)
settings_main_button = Button(150, 360, "images/settings_main.png", 3)
exit_button = Button(165, 430, "images/exit_main.png", 4)
resume_button = Button(135, 220, "images/resumebutton.png", 4)
exit_menu_button = Button(135, 375, "images/exitbutton.png", 4)
volume_on = Button(187,215, "images/settings/VolOn.png", 3.4)
volume_off = Button(187, 215, "images/settings/VolOff.png", 3.4)
broom = Button(187,327, "images/settings/ResetClear.png", 3.4)
confirm_reset = Button(175, 280, 'images/settings/Confirm.png', 4)
close_request = Button(86, 206, "images/settings/closebut.png", 0.03)
restart_button = Button(115,300, "images/restartbutton.png", 3)

    # Navigation
menu_button = Button(59, 10, 'images/menu_button.png', 0.75)
settings = Button(104, 10, "images/settings_button.png", 0.75)
left_arrow = Button(20, 275, "images/Left_Arrow.png", 4)
right_arrow = Button(430, 275, "images/Right_Arrow.png", 4)

    # Action Buttons
bed = Button(264, 193, "actions/bed.png", 5.28)
shower = Button(85, 90, "actions/shower.png", 5.1)
toilet = Button(296, 220, "actions/toilet.png", 5)
arcade_chair = Button(200, 370, "actions/arcade_chair.png", 5)
table = Button(109, 365, "actions/table.png", 5.2)
ref = Button(90, 80, "actions/ref.png", 5)
close_button = Button(90, 90, 'images/Ref_Exit.png', 3)

    # Food Images
banana = Button(135, 240, "images/food/banana.png", 5)
carrot = Button(190, 230, "images/food/carrot.png", 5)
coftea = Button(235, 230, "images/food/coftea.png", 5)
milk  = Button(290, 230, "images/food/milk.png", 5)
egg  = Button(145, 385, "images/food/egg.png", 5)
bread = Button(195, 390, "images/food/bread.png", 5)
chiki = Button(240, 390, "images/food/chiki.png", 5)
burger = Button(285, 390, "images/food/burger.png", 5)
plate = Button(206, 380, "images/plate.png", 3)


# Time settings
DAY_LENGTH_SECONDS = 10 * 60  # 10 minutes
start_time = time.time()
tamagotchi_day = 1

# === Drawing Utilities ===
def draw_IMG(img): # BG ONLY
    screen.blit(pygame.transform.scale(img, (WIDTH, HEIGHT)), (0, 0))

def draw_text(text, font, color, surface, x, y, center=False): # FOR DRAWING TEXT
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(topleft=(x, y))
    if center:
        text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

def draw_stat(img, x, y): # FOR DRAWING STATS
    screen.blit(pygame.transform.scale(img, (50, 50)), (x, y))

last_diddy_index = None  # To track which image was last hovered
def draw_hover_image(frame_index, base_pos, hover_pos, diddy_frame_index, player):
    global last_diddy_index

    player_frame = pygame.transform.scale(player_animation[frame_index], (160, 160))
    hover_frame = pygame.transform.scale(diddy_stat[diddy_frame_index], (50, 50))

    base_rect = player_frame.get_rect(topleft=base_pos)
    screen.blit(player_frame, base_pos)

    if base_rect.collidepoint(pygame.mouse.get_pos()):
        screen.blit(hover_frame, hover_pos)

        # If new hover image (diddy_frame_index) is different, play its sound
        if last_diddy_index != diddy_frame_index:
            if diddy_frame_index == 0:
                sound.happy.play()
            elif diddy_frame_index == 1:
                sound.neutral.play()
            elif diddy_frame_index == 2:
                sound.bored.play()
            elif diddy_frame_index == 3:
                sound.sad.play()
            elif diddy_frame_index == 4:
                sound.angry.play()

            last_diddy_index = diddy_frame_index
    else:
        last_diddy_index = None  # Reset when mouse not hovering

def draw_hover_static_image(base_image, base_pos, hover_frames, frame_index, hover_pos, base_size=None): # TO DRAW ZIDDY MOOD ON TOP OF PLAYER W/O ANIMATION
    if base_size:
        base_image = pygame.transform.scale(base_image, base_size)

    base_rect = base_image.get_rect(topleft=base_pos)
    screen.blit(base_image, base_pos)

    if base_rect.collidepoint(pygame.mouse.get_pos()):
        hover_img = hover_frames[frame_index]
        screen.blit(hover_img, hover_pos)

def update_frame(current_time, last_time, frame_index, frame_delay, frame_list): # CHANGES STATS ACCORDINGLY (DOES NOT LOOP)
    if current_time - last_time >= frame_delay:
        if frame_index < len(frame_list) - 1:
            frame_index += 1
        last_time = current_time
    return frame_index, last_time

def play_scene_animation(bg_frames, player_img=None, hover_frames=None, diddy_index=None, player_pos=None,
                         hover_pos=None, delay=0.1, sound_effect=None): # BG ANIMATION
    if sound_effect:
        sound_effect.play()

    for frame in bg_frames:
        # Draw background frame
        screen.blit(pygame.transform.scale(frame, (WIDTH, HEIGHT)), (0, 0))

        # Only draw player + hover if all required arguments are provided
        if all(arg is not None for arg in [player_img, hover_frames, diddy_index, player_pos, hover_pos]):
            draw_hover_static_image(player_img, player_pos, hover_frames, diddy_index, hover_pos, base_size=(160, 160))

        pygame.display.update()
        pygame.time.delay(int(delay * 1000))

def loop(current_time, last_time, frame_index, frame_delay, frame_list): # PLAYER ANIMATION LOOPS
    if current_time - last_time >= frame_delay:
        frame_index = (frame_index + 1) % len(frame_list)
        last_time = current_time
    return frame_index, last_time

def play_death_animation_with_bg(frames, bg_frames, index, pos=(160, 320), scale=(160, 160),
                                 delay=0.1, sound_effect=None):
    if sound_effect:
        sound_effect.play()

    if index < len(frames):
        bg_img = bg_frames[index % len(bg_frames)]  # Alternate between bg images
        draw_IMG(bg_img)

        frame_img = pygame.transform.scale(frames[index], scale)
        screen.blit(frame_img, pos)

        pygame.display.update()
        pygame.time.delay(int(delay * 1000))

        index += 1
    return index

def play_animation_with_bg(bg_img, animation_frames, pos, scale, delay=0.5, sound_effect=None):
    if sound_effect:
        sound_effect.play()

    for frame in animation_frames:
        draw_IMG(bg_img)  # Draw the background
        frame_img = pygame.transform.scale(frame, scale)
        screen.blit(frame_img, pos)
        pygame.display.update()
        pygame.time.delay(int(delay * 1000))


# === Room Draw Functions ===
def draw_room_bathroom(player, potty_frame_index, shower_frame_index, player_frame_index, diddy_frame_index):
    draw_IMG(bathroom)
    draw_hover_image(player_frame_index, (160, 320), (210, 270), diddy_frame_index, player)

    if shower.draw(screen):
        if shower_frame_index == 0:
            print("You are still clean!")
        elif 0 < shower_frame_index < 5:
            shower_frame_index -= 1
            sound.showering.play()
            sound.humming.play()
            play_scene_animation(shower_frames, delay=0.2)
        elif 5 <= shower_frame_index <= 10:
            shower_frame_index -= 2
            sound.showering.play()
            sound.humming.play()
            play_scene_animation(shower_frames, delay=0.2)

    if toilet.draw(screen):
        if potty_frame_index == 0:
            print("You don't have to potty yet!")
        elif 0 < potty_frame_index < 5:
            potty_frame_index -= 1
            draw_IMG(bathroom)
            play_animation_with_bg(bathroom, player_poop, pos=(50, 0), scale=(400, 600), delay=0.5,
                                   sound_effect=sound.pooping)
        elif 5 <= potty_frame_index <= 10:
            potty_frame_index -= 2
            draw_IMG(bathroom)
            play_animation_with_bg(bathroom, player_poop, pos=(50, 0), scale=(400, 600), delay=0.5,
                                   sound_effect=sound.pooping)

    if right_arrow.draw(screen):
        select_sound.play()
        return 2, potty_frame_index, shower_frame_index
    return 1, potty_frame_index, shower_frame_index

def draw_room_bedroom(player, bed_frame_index, sleep_frame_index, player_frame_index, diddy_frame_index):
    draw_hover_image(player_frame_index, (160, 320), (210, 270), diddy_frame_index, player)

    if bed.draw(screen):
        if sleep_frame_index == 0:
            print("You have enough energy!")
        elif 0 < sleep_frame_index < 8:
            sleep_frame_index -= 1
            draw_IMG(bed_frames[bed_frame_index])
            play_animation_with_bg(bed_frames[bed_frame_index], player_sleep, pos=(206, 163), scale=(190, 280),
                                   delay=0.5, sound_effect=sound.sleeping)
        elif 8 <= sleep_frame_index <= 10:
            sleep_frame_index = 5
            draw_IMG(bed_frames[bed_frame_index])
            play_animation_with_bg(bed_frames[bed_frame_index], player_sleep, pos=(206, 163), scale=(190, 280),
                                   delay=0.5, sound_effect=sound.sleeping)

    if left_arrow.draw(screen):
        select_sound.play()
        return 1, sleep_frame_index
    if right_arrow.draw(screen):
        select_sound.play()
        return 3, sleep_frame_index

    return 2, sleep_frame_index

selected_food = None
def draw_room_kitchen(player, hunger_frame_index, player_frame_index, diddy_frame_index, show_menu):
    global selected_food
    draw_IMG(kitchen)

    # Open menu when fridge clicked
    if ref.draw(screen):
        show_menu = True

    draw_hover_image(player_frame_index, (160, 280), (210, 230), diddy_frame_index, player)
    table.draw(screen)
    # Remove food when clicking plate or table
    if plate.draw(screen):
        if selected_food:
            if hunger_frame_index == 0:
                print("You are still full!")
            elif 0 < hunger_frame_index <= 10:
                selected_food = None
                hunger_frame_index -= 1
                play_animation_with_bg(kitchen, player_eat, pos=(160, 280), scale=(160, 90), delay=0.5
                                       ,sound_effect=sound.eating)

    def eating_selecting(food_button):
        global selected_food
        if food_button.draw(screen):
            selected_food = food_button  # Clone to plate
            return True
        return False

    if show_menu:
        draw_IMG(food_menu)
        if (
            eating_selecting(banana) or
            eating_selecting(bread) or
            eating_selecting(burger) or
            eating_selecting(carrot) or
            eating_selecting(chiki) or
            eating_selecting(coftea) or
            eating_selecting(egg) or
            eating_selecting(milk)
        ):show_menu = False
        if close_button.draw(screen):
            select_sound.play()
            show_menu = False


    # Draw cloned food on the plate
    if selected_food:
        screen.blit(
            selected_food.image,
            (
                plate.rect.centerx - selected_food.image.get_width() // 2,
                plate.rect.centery - selected_food.image.get_height() // 2
            )
        )


    if left_arrow.draw(screen):
        select_sound.play()
        return 2, hunger_frame_index, show_menu
    if right_arrow.draw(screen):
        select_sound.play()
        return 4, hunger_frame_index, show_menu

    return 3, hunger_frame_index, show_menu

def draw_room_arcade(player, diddy_frame_index):
    draw_IMG(arcade)
    draw_hover_static_image(player_back, (160, 250), diddy_stat, diddy_frame_index, (215, 200), (160,160))

    if arcade_chair.draw(screen):
        if diddy_frame_index == 0:
            print("You're not bored!")
        if 0 < diddy_frame_index <= 5:
            diddy_frame_index -= 1
            play_scene_animation(arcade_frames, player_back, diddy_stat, diddy_frame_index, (160, 250), (215, 200), )
            player.sleep_level += 1

    if left_arrow.draw(screen):
        select_sound.play()
        return 3, diddy_frame_index

    return 4, diddy_frame_index


# === Main Game Loop ===
def main():
    global start_time, tamagotchi_day
    force_reset_table()

    player = Androgynous()
    game_state = 0
    running = True 
    show_menu = False
    is_muted = False
    game_over = False

    # Animation Index
    arcade_frame_index = 0
    bed_frame_index = 0
    player_frame_index = 0
    diddy_frame_index = 0
    death_frame_index = 0

    # Animation Time
    arcade_frame_time = time.time()
    bed_frame_time = time.time()
    player_frame_time = time.time()
    diddy_frame_time = time.time()

    # Animation Delays (seconds per frame)
    arcade_frame_delay = 0.2 
    bed_frame_delay = 150
    player_frame_delay = 0.5
    diddy_frame_delay = 120

    while running:
        for event in pygame.event.get():
            player.save_to_db()
            if event.type == pygame.QUIT:
                running = False

        # Update day counter
        elapsed = time.time() - start_time
        if elapsed >= DAY_LENGTH_SECONDS:
            tamagotchi_day += 1 # PLAYER's AGE
            start_time = time.time()

        # === GLOBAL STAT UPDATES ===
        current_time = time.time()

        # STAT animation updates
        player.sleep_level, player.sleep_timer = update_frame(current_time, player.sleep_timer, player.sleep_level, player.sleep_delay, sleep_stat)
        player.potty_level, player.potty_timer = update_frame(current_time, player.potty_timer, player.potty_level, player.potty_delay, toilet_stat)
        player.shower_level, player.shower_timer = update_frame(current_time, player.shower_timer, player.shower_level, player.shower_delay, toilet_stat)
        player.hunger_level, player.hunger_timer = update_frame(current_time, player.hunger_timer, player.hunger_level, player.hunger_delay, hunger_stat)
        diddy_frame_index, diddy_frame_time = update_frame(current_time, diddy_frame_time, diddy_frame_index, diddy_frame_delay, diddy_stat)

        arcade_frame_index, arcade_frame_time = update_frame(current_time, arcade_frame_time, arcade_frame_index, arcade_frame_delay, arcade_frames)
        bed_frame_index, bed_frame_time = loop(current_time, bed_frame_time, bed_frame_index, bed_frame_delay, bed_frames)
        player_frame_index, player_frame_time = loop(current_time, player_frame_time, player_frame_index, player_frame_delay, player_animation)

        if (
            player.sleep_level == 10 and
            player.potty_level == 10 and
            player.shower_level == 10 and
            player.hunger_level == 10
        ):
            game_over = True

        if game_over:
            if death_frame_index < len(player_death):
                death.play()
                stop_bgm()
                play_death_music()
                death_backgrounds = [pygame.Surface((WIDTH, HEIGHT)), pygame.Surface((WIDTH, HEIGHT))]
                death_backgrounds[0].fill((0, 0, 0))
                death_backgrounds[1].fill((255, 255, 255))
                death_frame_index = play_death_animation_with_bg(player_death, death_backgrounds, death_frame_index)
            else:
                if death_frame_index == len(player_death):
                    player.sleep_level = 0
                    player.potty_level = 0
                    player.shower_level = 0
                    player.hunger_level = 0

                    # ERASE DATABASE ENTRY
                    conn = create_connection()
                    c = conn.cursor()
                    c.execute("DELETE FROM player_data")
                    conn.commit()
                    conn.close()

                    death_frame_index += 1
                screen.fill((0, 0, 0))
                draw_IMG(gameoverBG)
                screen.blit(pygame.transform.scale(player_death[16], (150, 125)), (160, 370))
                if restart_button.draw(screen):
                    select_sound.play()
                    play_bgm()
                    player = Androgynous()
                    game_over = False
                    game_state = 0
                    death_frame_index = 0
            pygame.display.update()
            continue

        screen.fill((0, 0, 0))

        # ROOMS FUNCTION IMPLEMENTATIONS

        if game_state == 0:  # MAIN MENU
            draw_IMG(titlescreen)
            draw_IMG(home_TEXT)
            if play_button.draw(screen):
                select_sound.play()
                game_state = 2
            if settings_main_button.draw(screen):
                select_sound.play()
                pass
            if exit_button.draw(screen):
                select_sound.play()
                running = False


        else:
            if game_state == 1: # BATHROOM
                game_state, player.potty_level, player.shower_level = draw_room_bathroom(
                    player, player.potty_level, player.shower_level, player_frame_index, diddy_frame_index)
            elif game_state == 2: # BEDROOM
                draw_IMG(bed_frames[bed_frame_index])
                game_state, player.sleep_level = draw_room_bedroom(
                    player, bed_frame_index, player.sleep_level, player_frame_index, diddy_frame_index)
            elif game_state == 3: # KITCHEN
                game_state, player.hunger_level, show_menu = draw_room_kitchen(player, player.hunger_level,
                                                                               player_frame_index, diddy_frame_index,
                                                                               show_menu)
            elif game_state == 4: # ARCADE
                game_state, diddy_frame_index = draw_room_arcade(player, diddy_frame_index)

            # UTILITIES

            if menu_button.draw(screen):
                select_sound.play()
                paused = True
                while paused:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            exit()
                    draw_IMG(menu)
                    if resume_button.draw(screen):
                        select_sound.play()
                        paused = False
                    elif exit_menu_button.draw(screen):
                        select_sound.play()
                        game_state = 0
                        paused = False
                    pygame.display.update()

            if settings.draw(screen):
                select_sound.play()
                open_settings = True
                while open_settings:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            exit()
                    screen.blit(pygame.transform.scale(SettingsMenu, (225, 300)), (125, 150))

                    if is_muted:
                        if volume_off.draw(screen):
                            is_muted = False
                            pygame.mixer.unpause()
                            pygame.mixer.music.set_volume(0.2)  # Restore music volume
                    else:
                        if volume_on.draw(screen):
                            select_sound.play()
                            is_muted = True
                            pygame.mixer.pause()
                            pygame.mixer.music.set_volume(0.0)  # Mute music

                    if close_button.draw(screen):
                        select_sound.play()
                        open_settings = False

                    if broom.draw(screen):
                        select_sound.play()
                        open_settings = False
                        reset_settings = True
                        while reset_settings:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    exit()
                            # Draw confirmation popup
                            screen.blit(pygame.transform.scale(reset_ques, (230, 140)), (125, 180))
                            if confirm_reset.draw(screen):
                                # Erase saved progress from DB
                                conn = create_connection()
                                c = conn.cursor()
                                c.execute("DELETE FROM player_data")
                                conn.commit()
                                conn.close()

                                # Reinitialize game variables
                                player = Androgynous()
                                game_state = 0
                                game_over = False
                                tamagotchi_day = 0

                                # Restart BGM
                                stop_bgm()
                                play_bgm()

                                print("Data reset confirmed!")
                                reset_settings = False
                            elif close_request.draw(screen):
                                select_sound.play()
                                reset_settings = False

                            pygame.display.update()

                    pygame.display.update()

            # Draw all stats regardless of room
            draw_stat(sleep_stat[player.sleep_level], 120, 548)
            draw_stat(toilet_stat[player.potty_level], 180, 548)
            draw_stat(shower_stat[player.shower_level], 240, 548)
            draw_stat(hunger_stat[player.hunger_level], 300, 548)
            draw_text("Ziddy Age: ", CutePixel, (255, 255, 255), screen, 210, 30, center=True)
            draw_text(str(tamagotchi_day), CutePixel, (255, 255, 255), screen, 280, 30, center=True)

        pygame.display.update()

    pygame.quit()

main()


