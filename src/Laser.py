from src.GameValues import *
from src.classes.Vector2D import Vector2D, number_types
from src.classes.GameObject import GameObject
import pygame
from enum import Enum



class Laser(GameObject):

    class LaserState(Enum):
        Anticipation = 1
        Attack = 2
        Recovery = 3

    class LaserMovement(Enum):
        Constant = 1
        AcceleratingStart = 2
        DeceleratingEnd = 3


    def __init__(self,
        begin_point: "Vector2D",
        direction: "Vector2D",
        time: number_types, #ms
        width: number_types = 10,
        color: tuple = (255, 0, 0),
        laser_rotation_speed: number_types = 0)-> None:

        super().__init__(begin_point) #starting position
        self.direction = (direction/abs(direction))*(LASER_LENGTH**2)
        self.width = width
        self.starting_width = width
        self.color = color
        self.state = Laser.LaserState.Anticipation
        self.movement_type = Laser.LaserMovement.Constant
        self.rotation_speed = laser_rotation_speed
        self.cooldown = LASER_ANTICIPATION_TIME
        self.time_to_execute = time


    def main(self, clock: "pygame.time.Clock", rotation: number_types = 0, new_position: "Vector2D" = None):
        self.cooldown -= clock.get_time()
        self.time_to_execute -= clock.get_time()
        self.direction.angle_rotate(rotation)
        if new_position:
            self.position = new_position
        self.__evaluate_state()

        if self.state == Laser.LaserState.Recovery:
            self.width = (self.starting_width*(self.time_to_execute/LASER_ANTICIPATION_TIME))

    def render(self, display: "pygame.Surface"):
        if self.state == Laser.LaserState.Anticipation:
            new_color = (self.color[0]/2, self.color[1]/2, self.color[2]/2)
            pygame.draw.line(display, new_color, tuple(self.position), tuple(self.direction), self.width)
        elif self.state == Laser.LaserState.Attack:
            pygame.draw.line(display, self.color, tuple(self.position), tuple(self.direction), self.width)
        else:
            pygame.draw.line(display, self.color, tuple(self.position), tuple(self.direction), round(self.width))

    def __evaluate_state(self):
        if self.cooldown<=0:
            if self.state == Laser.LaserState.Anticipation:
                self.state = Laser.LaserState.Attack
                self.cooldown = self.time_to_execute-LASER_ANTICIPATION_TIME
            elif self.state == Laser.LaserState.Attack:
                self.state = Laser.LaserState.Recovery
                self.time_to_expire = LASER_ANTICIPATION_TIME
                self.cooldown = LASER_ANTICIPATION_TIME

    def set_type_of_laser(self,
        move_types: list["Laser.LaserMovement"] = [LaserMovement.Constant],
        increase_rotation_speed: number_types = 0, #px/s
        max_rotation_speed: number_types = 0, #px/s
        min_rotation_speed: number_types = 0, #px/s
        )->None:
        if not isinstance(move_types, list):
            move_types = [move_types]
        self.movement_types = move_types
        self.increase_rotation_speed = increase_rotation_speed
        self.max_rotation_speed = max_rotation_speed
        self.max_rotation_speed = min_rotation_speed



