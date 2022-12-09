from typing import Union
from classes.Vector2D import Vector2D, number_types
from classes.GameObject import GameObject
import pygame


class Bullet(GameObject):
    def __init__(self, raduis : number_types, speed : number_types, direction : "Vector2D"):
        self.speed = speed
        self.raduis = raduis
        self.direction = direction

    def main(self, display):
        pygame.draw.circle(display, (0, 255, 0), (self.position.x, self.position.y, self.radius))