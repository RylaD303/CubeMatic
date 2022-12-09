from typing import Union
from Vector2D import Vector2D, number_types
import pygame



class GameObject():
    def __init__(self, x: number_types, y: number_types) -> "GameObject":
        self.position = Vector2D(x,y)