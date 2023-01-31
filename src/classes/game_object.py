from typing import Union
from src.classes.vector_2d import Vector2D, number_types
import pygame



class GameObject():
    """Base class for every object in the game."""

    def __init__(self, position : "Vector2D") -> None:
        """
        Initialises Game object.
        Sets position, visibility and radius of collision.
        """
        self.position = position
        self.visible = True
        self.radius = 0

    def centre_position(self) -> Vector2D:
        return self.position

    def is_colliding_with(self, other) -> bool:
        pass

    def main(self) -> None:
        pass

    def render(self) -> None:
        pass
