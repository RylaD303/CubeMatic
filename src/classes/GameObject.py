from typing import Union
from src.classes.Vector2D import Vector2D, number_types
import pygame



class GameObject():
    def __init__(self, position : "Vector2D") -> "GameObject":
        self.position = position