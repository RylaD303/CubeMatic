import pygame, sys
from pygame.locals import *
from src.Player import Player
from src.Bullet import Bullet
from src.classes.Vector2D import Vector2D

pygame.init()
clock = pygame.time.Clock()
player = Player(Vector2D(20,20))
WINDOW_SIZE =(800,400)

screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)

while True:
    screen.fill((0,0,0))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    player.main(screen)
    pygame.display.update()
    clock.tick(60)
