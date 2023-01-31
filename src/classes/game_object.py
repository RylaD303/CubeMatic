from typing import Union
from src.classes.vector_2d import Vector2D, number_types
import pygame



class GameObject():
    """Abstract base class for every object in the game."""

    def __init__(self, position : "Vector2D") -> None:
        """
        Initialises Game object.
        Sets position, visibility and radius of collision.
        """
        self.position = position
        self.visible = True
        self.radius = 0
        self.valid = True

    def is_valid(self) -> None:
        """
        Invalidates game object so the collision handler can detect
        it should be removed.
        """
        return self.valid

    def invalidate(self) -> None:
        self.valid = False

    def centre_position(self) -> Vector2D:
        return self.position

    def is_colliding_with(self, other) -> bool:
        pass

    def main(self) -> None:
        pass

    def render(self) -> None:
        pass