from typing import Union
from classes.Vector2D import Vector2D
from classes.GameObject import GameObject
import pygame


class Player(GameObject):
    def __init__(self, health_points, speed, width, height):
        self.health_points = health_points
        self.speed = speed
        self.width = width
        self.height = height

    def main(self, display):
        pygame.draw.rect(display, (0, 255, 0), (self.position.x, self.position.y, self.width, self.height))