from typing import Union
from src.classes.Vector2D import Vector2D, number_types
from src.classes.GameObject import GameObject
import pygame


class Bullet(GameObject):
    def __init__(
        self,
        starting_position: "Vector2D",
        direction: "Vector2D",
        speed : number_types = 6,
        radius: number_types = 2) -> None:
        """Initialises bullet."""
        super().__init__(starting_position)
        self.speed = speed
        self.direction = direction
        self.radius = radius

        if self.position == self.direction :
            self.direction+=1

        self.movement =  speed*(self.direction - self.position)/abs(self.direction - self.position)

    def main(self) -> None:
        """Handles the bullet frame by frame"""
        self.__move()

    def __move(self) -> None:
        """Moves the bullet by it's movement vector."""
        self.position += self.movement

    def render(self, display : "pygame.Surface"):
        """Displays bullet on screen"""
        pygame.draw.circle(display, (0, 255, 0), (self.position.x, self.position.y), self.radius)