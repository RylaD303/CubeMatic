import pygame, sys
from pygame.locals import *
from src.Player import Player
from src.Bullet import Bullet
from src.classes.Vector2D import Vector2D

pygame.init()
clock = pygame.time.Clock()

PLAYER_START = Vector2D(20,20)
PLAYER_SPEED = 8
PLAYER_SCALE = Vector2D(32, 32)

WINDOW_SIZE =(1400,700)

START_OF_MAP = Vector2D(0,0)
END_OF_MAP = Vector2D(*WINDOW_SIZE)


player = Player(PLAYER_START, PLAYER_SPEED, pygame.image.load('src/sprites/Player1.png'), *tuple(PLAYER_SCALE))
player_movement = [False,False,False,False]
player_firing = False

bullets_fired: set[Bullet] = set()
resizable_screen = pygame.display.set_mode(WINDOW_SIZE, RESIZABLE)
screen = resizable_screen.copy()
screen_scaling = 1

game_running = True

while game_running:
    screen.fill((0,0,0))

    for event in pygame.event.get():
        if event.type == QUIT:
            game_running = False
            pygame.quit()
            sys.exit()

        elif event.type == VIDEORESIZE:
            resizable_screen = pygame.display.set_mode((event.size[0],event.size[0]/2), RESIZABLE)
            screen_scaling = event.size[0]/WINDOW_SIZE[0]

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                player_movement[0] = True
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                player_movement[1] = True
            if event.key == pygame.K_UP or event.key == ord('w'):
                player_movement[2] = True
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                player_movement[3] = True

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                player_movement[0] = False
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                player_movement[1] = False
            if event.key == pygame.K_UP or event.key == ord('w'):
                player_movement[2] = False
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                player_movement[3] = False

        elif event.type == pygame.MOUSEBUTTONDOWN :
            if event.button == 1:              #left mouse click
                player_firing = True
            if event.button == 2:              #right mouse click
                pass

        elif event.type == pygame.MOUSEBUTTONUP :
            if event.button == 1:
                player_firing = False
            if event.button == 2:
                pass


    if player_firing:
        bullets_fired.add(Bullet(player.position + PLAYER_SCALE/2, Vector2D(*pygame.mouse.get_pos())/screen_scaling))
    player.main(screen, player_movement)


    bullets_to_remove: set[Bullet]= set()
    for bullet in bullets_fired:
        bullet.main(screen)
        if  bullet.position.x <= START_OF_MAP.x or\
            bullet.position.x >= END_OF_MAP.x or\
            bullet.position.y <= START_OF_MAP.y or\
            bullet.position.y >= END_OF_MAP.y:
            bullets_to_remove.add(bullet)

    for bullet in bullets_to_remove:
        bullets_fired.remove(bullet)

    resizable_screen.blit(pygame.transform.scale(screen, resizable_screen.get_rect().size), (0,0))
    pygame.display.flip()

    clock.tick(60)
