import pygame, sys
from pygame.locals import *
from src.Player import Player
from src.Bullet import Bullet
from src.classes.Vector2D import Vector2D

pygame.init()
clock = pygame.time.Clock()

PLAYER_START = Vector2D(20,20)
PLAYER_SPEED = 4

WINDOW_SIZE =(800,400)

START_OF_MAP = Vector2D(0,0)
END_OF_MAP = Vector2D(*WINDOW_SIZE)


player = Player(PLAYER_START, PLAYER_SPEED)
player_movement = [False,False,False,False]
player_firing = False

bullets_fired: set[Bullet] = set()

screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)

while True:
    screen.fill((0,0,0))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                player_movement[0] = True
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                player_movement[1] = True
            if event.key == pygame.K_UP or event.key == ord('w'):
                player_movement[2] = True
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                player_movement[3] = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                player_movement[0] = False
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                player_movement[1] = False
            if event.key == pygame.K_UP or event.key == ord('w'):
                player_movement[2] = False
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                player_movement[3] = False

        if event.type == pygame.MOUSEBUTTONDOWN :
            if event.button == 1:              #left mouse click
                player_firing = True
            if event.button == 2:              #right mouse click
                pass

        if event.type == pygame.MOUSEBUTTONUP :
            if event.button == 1:
                player_firing = False
            if event.button == 2:
                pass


    if player_firing:
        bullets_fired.add(Bullet(player.position, Vector2D(*pygame.mouse.get_pos())))
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

    pygame.display.update()

    clock.tick(60)
