from src.GameValues import *
from src.classes.Vector2D import Vector2D, number_types
from src.classes.GameObject import GameObject
import pygame
from enum import Enum



class LaserState(Enum):
    Anticipation = 1
    Attack = 2
    Recovery = 3


class Laser(GameObject):
    def __init__(self,
        begin_point: "Vector2D",
        direction: "Vector2D",
        time: number_types, #ms
        width: number_types = 10,
        color: tuple = (255, 0, 0))-> None:

        super().__init__(begin_point) # starting position
        self.direction = (direction/abs(direction))*(LASER_LENGTH**2)
        self.width = width
        self.color = color
        self.active = False
        self.state = LaserState.Anticipation
        self.cooldown = 1000
        self.time_to_execute = time


    def main(self, clock: "pygame.time.Clock", rotation: number_types = 0, new_position: "Vector2D" = None):
        self.cooldown -= clock.get_time()
        self.time_to_execute -= clock.get_time()
        self.direction.angle_rotate(rotation)
        if new_position:
            self.position = new_position
        self.__evaluate_state()

    def render(self, display: "pygame.Surface"):
        if self.state == LaserState.Anticipation:
            new_color = (self.color[0]/2, self.color[1]/2, self.color[2]/2)
            pygame.draw.line(display, new_color, tuple(self.position), tuple(self.direction), self.width)
        elif self.state == LaserState.Attack:
            pygame.draw.line(display, self.color, tuple(self.position), tuple(self.direction), self.width)
        elif self.state == LaserState.Recovery:
            pygame.draw.line(display, self.color, tuple(self.position), tuple(self.direction), self.width)

    def __evaluate_state(self):
        if self.cooldown<=0:
            if self.state == LaserState.Anticipation:
                self.state = LaserState.Attack
                self.cooldown = self.time_to_execute-1000
            elif self.state == LaserState.Attack:
                self.state == LaserState.Recovery
                self.time_to_expire = 1000
                self.cooldown = 1000


