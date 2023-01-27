from typing import Union
from math import sin
from src.classes.Vector2D import Vector2D, number_types
from src.classes.GameObject import GameObject
import pygame

class MapTile(GameObject):
    """The MapTile Game object. Stops player from moving around. Stops projectiles."""
    def __init__(
        self,
        position: "Vector2D",
        tile_sprite: "pygame.Surface",
        rotation: number_types = 0,
        width: number_types = 64,
        height: number_types = 64) -> "None":
        """Initialisation of MapTile object."""

        super().__init__(position)
        self.width = width
        self.height = height
        self.sprite = pygame.transform.scale(tile_sprite, (self.width, self.height))
        self.rotation = rotation

    def render(self, display: "pygame.Surface") -> None:
        """Draws the MapTile on the screen."""
        rotated_sprite = pygame.transform.rotate(self.sprite, self.rotation)
        display.blit(\
            rotated_sprite,
            (self.position.x - (rotated_sprite.get_width() - self.sprite.get_width())/2,
            self.position.y - (rotated_sprite.get_height() - self.sprite.get_height())/2))