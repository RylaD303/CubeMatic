import pygame, sys
from pygame.locals import *
from src.Player import Player
from src.Bullet import Bullet
from src.classes.Vector2D import Vector2D

pygame.init()
clock = pygame.time.Clock()

PLAYER_START = Vector2D(20,20)
PLAYER_SPEED = 5
player = Player(PLAYER_START, PLAYER_SPEED)
player_movement = [False,False,False,False]
WINDOW_SIZE =(800,400)

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

    player.main(screen, player_movement)
    pygame.display.update()
    clock.tick(60)
