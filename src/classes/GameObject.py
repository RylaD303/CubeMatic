from typing import Union
from src.classes.Vector2D import Vector2D, number_types
import pygame



class GameObject():
    """Base calss for every object in the game. Contatins position"""

    def __init__(self, position : "Vector2D") -> "GameObject":
        """Initialises Game object. Sets position."""
        self.position = position