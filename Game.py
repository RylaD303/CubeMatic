import pygame, sys
from pygame.locals import *
from src import Bullet, Player


pygame.init()

WINDOW_SIZE =(400,400)

screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
