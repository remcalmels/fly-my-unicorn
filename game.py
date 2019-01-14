# v0.1

import pygame
import time
from random import randint


# Constants
SURFACE_W = 800
SURFACE_H = 600
CAPTION = "Fly my unicorn!"
BG_COLOR = (126, 229, 255)
MOVEMENT_STEP = 4
SURFACE_MARGIN = 0
FONT_NAME = "BradBunR.ttf"
UNICORN_W = 41
UNICORN_H = 74
CLOUD_W = 179
CLOUD_H = 123
CLOUD_MAX_SPACE = 4
CLOUD_MIN_SPEED = 3
SCORE_FONT_SIZE = 25
high_score = 0


def init_surface(resolution, caption, bgcolor):
    global surface
    surface = pygame.display.set_mode(resolution)
    pygame.display.set_caption(caption)
    global clock
    clock = pygame.time.Clock()
    surface.fill(bgcolor)
    pygame.display.update()


def init_unicorn():
    global unicorn_sprite
    unicorn_sprite = pygame.sprite.Sprite()
    unicorn_sprite.image = pygame.image.load("assets/unicorn.png").convert_alpha()
    unicorn_sprite.rect = unicorn_sprite.image.get_rect()
    unicorn_sprite.mask = pygame.mask.from_surface(unicorn_sprite.image)


def init_clouds():
    global cloud1_sprite, cloud2_sprite
    cloud1_sprite = pygame.sprite.Sprite()
    cloud1_sprite.image = pygame.image.load("assets/cloud1.png").convert_alpha()
    cloud1_sprite.rect = cloud1_sprite.image.get_rect()
    cloud1_sprite.mask = pygame.mask.from_surface(cloud1_sprite.image)
    cloud2_sprite = pygame.sprite.Sprite()
    cloud2_sprite.image = pygame.image.load("assets/cloud2.png").convert_alpha()
    cloud2_sprite.rect = cloud2_sprite.image.get_rect()
    cloud2_sprite.mask = pygame.mask.from_surface(cloud2_sprite.image)


def init():
    pygame.init()
    init_surface((SURFACE_W, SURFACE_H), CAPTION, BG_COLOR)
    init_unicorn()
    init_clouds()


# Fix unicorn position
def move_unicorn(position):
    surface.fill(BG_COLOR)
    unicorn_sprite.rect.topleft = position
    surface.blit(unicorn_sprite.image, unicorn_sprite.rect.topleft)


# Fix clouds positions
def move_clouds(cloud1_pos, cloud2_pos):
    cloud1_sprite.rect.topleft = cloud1_pos
    surface.blit(cloud1_sprite.image, cloud1_sprite.rect.topleft)
    cloud2_sprite.rect.topleft = cloud2_pos
    surface.blit(cloud2_sprite.image, cloud2_sprite.rect.topleft)


def create_text(font_size, msg, position, center, color):
    text_font = pygame.font.Font("assets/" + FONT_NAME, font_size)
    text_txt = text_font.render(msg, True, color)
    text_rect = text_txt.get_rect()
    if center:
        text_rect.center = position
    else:
        text_rect.x, text_rect.y = position
    return text_txt, text_rect


def show_message():
    gameover_txt, gameover_rect = create_text(150, "PERDU !", (SURFACE_W/2, (SURFACE_H/2 - 50)), True, (0, 0, 0))
    surface.blit(gameover_txt, gameover_rect)
    restart_txt, restart_rect = create_text(40, "Appuyez sur entrée pour recommencer", (SURFACE_W/2, (SURFACE_H/2 + 50)), True, (0, 0, 0))
    surface.blit(restart_txt, restart_rect)
    pygame.display.update()


def show_score():
    current_score_txt, current_score_rect = create_text(SCORE_FONT_SIZE, "SCORE : " + str(current_score), (10, 20 - SCORE_FONT_SIZE/2), False, (255, 255, 255))
    surface.blit(current_score_txt, current_score_rect)
    high_score_txt, high_score_rect = create_text(SCORE_FONT_SIZE, "RECORD : " + str(high_score), (SURFACE_W/2, 20), True, (255, 255, 255))
    surface.blit(high_score_txt, high_score_rect)
    level_txt, level_rect = create_text(SCORE_FONT_SIZE, "NIVEAU : " + str(level), (SURFACE_W - 100, SCORE_FONT_SIZE/2), False, (255, 255, 255))
    surface.blit(level_txt, level_rect)
    pygame.display.update()


def quit_game():
    pygame.quit()
    quit()


def get_action():
    for event in pygame.event.get([pygame.KEYUP, pygame.QUIT]):
        if event.type == pygame.QUIT:
            quit_game()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RETURN:
                pygame.event.clear()
                return True
    return False


def game_over():
    show_message()

    global high_score
    if high_score < current_score:
        high_score = current_score
        show_score()

    while not get_action():
        clock.tick()
    main()


def cloud_random_y_pos():
    global cloud1_y_pos, cloud2_y_pos
    cloud_space = randint(UNICORN_H * cloud_min_space, UNICORN_H * CLOUD_MAX_SPACE)
    cloud1_y_pos = randint(-CLOUD_H + SURFACE_MARGIN, SURFACE_H/4)
    cloud2_y_pos = randint(cloud1_y_pos + cloud_space, SURFACE_H - SURFACE_MARGIN)


def main():

    init()

    # Initial unicorn position
    unicorn_x_pos = 50
    unicorn_y_pos = 250
    unicorn_y_movement = 0

    # Initial clouds positions
    global cloud_min_space
    cloud_min_space = 2
    cloud_speed = CLOUD_MIN_SPEED
    cloud_x_pos = SURFACE_W - 100
    cloud_random_y_pos()

    # Score
    global current_score
    current_score = 0
    global level
    level = 0

    end_event = False
    while not end_event:
        for event in pygame.event.get():

            # Up
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    unicorn_y_movement = -MOVEMENT_STEP

            # Down
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    unicorn_y_movement = MOVEMENT_STEP - (MOVEMENT_STEP // 2)

            # Quit event
            if event.type == pygame.QUIT:
                end_event = True

        unicorn_y_pos += unicorn_y_movement
        if unicorn_y_pos > SURFACE_H - SURFACE_MARGIN or unicorn_y_pos < - (UNICORN_H - SURFACE_MARGIN):
            game_over()
        else:
            move_unicorn((unicorn_x_pos, unicorn_y_pos))
            move_clouds((cloud_x_pos, cloud1_y_pos), (cloud_x_pos, cloud2_y_pos))
        cloud_x_pos -= cloud_speed

        # Collision ? (with sprite masks)
        if pygame.sprite.collide_mask(unicorn_sprite, cloud1_sprite) or pygame.sprite.collide_mask(unicorn_sprite, cloud2_sprite):
            game_over()

        # Reappearance of clouds ?
        if cloud_x_pos < -CLOUD_W:
            cloud_x_pos = SURFACE_W
            cloud_random_y_pos()

        # Score update
        current_score+=1
        if current_score % 500 == 0:
            cloud_speed += 1
            level += 1
        show_score()

        pygame.display.update()

    # End of game
    quit_game()


main()










