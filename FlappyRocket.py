import pygame
import sys
import random


def draw_bg():
    window.blit(bg, (bg_x, 0))
    window.blit(bg, (bg_x + bg.get_width(), 0))


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(430, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(430, random_pipe_pos - 200))
    return bottom_pipe, top_pipe


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 600:
            window.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            window.blit(flip_pipe, pipe)


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= speed
    return pipes


def check_collision(pipes):
    for pipe in pipes:
        if player_rect.colliderect(pipe):
            return False
    if player_rect.top <= -100 or player_rect.top >= 700:
        return False
    return True


def rotate_player(player):
    new_player = pygame.transform.rotozoom(player, 0 - player_movement * 3.5, 1)
    return new_player


pygame.init()
window = pygame.display.set_mode((400, 600))
pygame.display.set_caption("Flappy Rocket")
pygame.display.set_icon(pygame.image.load("_spaceship_.png"))
clock = pygame.time.Clock()

# game variables
gravity = 0.25
player_movement = 0
speed = 3
game_active = True

player_surface = pygame.image.load("_spaceship_.png")
player_surface = pygame.transform.scale(player_surface, (50, 50))
player_surface = pygame.transform.rotate(player_surface, -90)
player_rect = player_surface.get_rect(center=(50, 300))

pipe_surface = pygame.image.load("pipe-green.png")
pipe_surface = pygame.transform.scale(pipe_surface, (70, 500))
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1800)
pipe_height = [250, 300, 350, 400, 450, 500]

bg = pygame.image.load("Background.png").convert()
bg_x = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_SPACE and game_active:
                player_movement = -7.5
            if event.key == pygame.K_SPACE and game_active == False:
                pipe_list.clear()
                player_rect.center = (50, 300)
                player_movement = -5
                speed = 3
                game_active = True

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

    window.fill((81, 120, 181))
    bg_x -= speed / 4
    draw_bg()
    speed += 0.0001

    if game_active:
        # player
        player_movement += gravity
        rotated_player = rotate_player(player_surface)
        player_rect.centery += player_movement
        window.blit(rotated_player, player_rect)
        game_active = check_collision(pipe_list)

        # pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

    # background movement
    if bg_x <= -400:
        bg_x = 0

    pygame.display.update()
    clock.tick(60)
