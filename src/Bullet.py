from typing import Union
from src.classes.Vector2D import Vector2D, number_types
from src.classes.GameObject import GameObject
import pygame


class Bullet(GameObject):
    def __init__(
        self,
        starting_position: "Vector2D",
        direction: "Vector2D",
        radius: number_types = 1,
        speed : number_types = 6) -> "None":
        """Initialises bullet."""
        super().__init__(starting_position)
        self.speed = speed
        self.direction = direction
        self.radius = radius