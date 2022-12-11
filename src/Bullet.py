from typing import Union
from src.classes.Vector2D import Vector2D, number_types
from src.classes.GameObject import GameObject
import pygame


class Bullet(GameObject):
    def __init__(self,
                starting_position: "Vector2D",
                direction: "Vector2D",
                radius: number_types = 1,
                speed : number_types = 6):

        self.speed = speed
        self.position = starting_position
        self.radius = radius
        self.direction = direction

    def main(self, display):
        pygame.draw.circle(display, (0, 255, 0), (self.position.x, self.position.y), self.radius)