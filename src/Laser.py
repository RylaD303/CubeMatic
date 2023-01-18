from src.GameValues import *
from src.classes.Vector2D import Vector2D, number_types
from src.classes.GameObject import GameObject
import pygame

class Laser(GameObject):
    def __init__(self,
        begin_point: "Vector2D",
        direction: "Vector2D",
        width: number_types,
        color: tuple = (255, 0, 0))-> None:

        super.__init__(begin_point) # starting position
        self.direction = direction
        self.width = width
        self.color = color


    def main(self, new_position: "Vector2D", rotation: number_types = 0):
        self.direction.angle_rotate(rotation)
        self.position = new_position

    def render(self, display: "pygame.Surface"):
        pygame.draw.line(display, self.color, tuple(self.position), tuple(self.direction), self.width)

