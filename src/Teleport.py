from typing import Union
from src.classes.Vector2D import Vector2D, number_types
from src.classes.GameObject import GameObject
import pygame

MAX_HOLD_TIME = 300

class Teleport(GameObject):
    def __init__(
        self,
        starting_position: "Vector2D",
        direction: "Vector2D",
        speed : number_types = 6,
        radius: number_types = 4) -> "None":
        """Initialises teleportation device."""
        super().__init__(starting_position)
        self.speed = speed
        self.direction = direction
        self.radius = radius
        self.time_remaining = MAX_HOLD_TIME #in frames
        if self.position == self.direction :
            self.direction+=1
        self.movement =  speed*(self.direction - self.position)/abs(self.direction - self.position)

    def main(self, display, player):
        """Displays the teleportation device on screen and moves it."""
        if self.time_remaining>MAX_HOLD_TIME/2:
            self.__move()
        self.time_remaining -= 1
        color = (255 - self.time_remaining*255/MAX_HOLD_TIME, 255, self.time_remaining*255/MAX_HOLD_TIME)
        pygame.draw.circle(display, color, (self.position.x, self.position.y), self.radius)

    def __move(self):
        """Moves the teleportation device by it's movement vector.
        Depending on the remaining time the movement will decrease"""
        speed_scaling = (self.time_remaining - MAX_HOLD_TIME/2)/MAX_HOLD_TIME
        self.position += self.movement*(speed_scaling)
        print(self.position)