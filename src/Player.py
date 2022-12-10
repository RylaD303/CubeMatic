from typing import Union
from src.classes.Vector2D import Vector2D, number_types
from src.classes.GameObject import GameObject
import pygame


class Player(GameObject):
    def __init__(self, position : "Vector2D", health_points : number_types = 1,
    speed : number_types = 5, width : number_types = 20, height : number_types = 20) -> "Player":

        super().__init__(position)
        self.health_points = health_points
        self.speed = speed
        self.width = width
        self.height = height

    def main(self, display) -> None:
        pygame.draw.rect(display, (0, 255, 0), (self.position.x, self.position.y, self.width, self.height))