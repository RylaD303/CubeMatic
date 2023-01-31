from src.game_values import *
from src.classes.vector_2d import Vector2D, number_types
from src.classes.game_object import GameObject
import pygame
from enum import Enum

WHITE = (255, 255 ,255)

class Laser(GameObject):
    """
    Laser object for the boss attacks.

    Handles own movement and chagne of states.
    """
    class LaserState(Enum):
        """Enum for laser state"""
        Anticipation = 1
        Attack = 2
        Recovery = 3

    class LaserMovement(Enum):
        """Enum to describe the laser movements"""
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
        """
        Initialises the Laser.

        Parameters:
        """
        super().__init__(begin_point) #starting position
        self.direction = (direction/abs(direction))*(LASER_LENGTH**2)
        self.width = width
        self.starting_width = width
        self.color = color
        self.state = Laser.LaserState.Anticipation
        self.movement_types = [Laser.LaserMovement.Constant]
        self.rotation_speed = laser_rotation_speed
        self.cooldown = LASER_ANTICIPATION_TIME
        self.time_to_execute = time


    def main(self, clock: "pygame.time.Clock", new_position: "Vector2D" = None):
        self.cooldown -= clock.get_time()
        self.time_to_execute -= clock.get_time()
        self.direction.angle_rotate(self.rotation_speed*clock.get_time()/1000)
        if new_position:
            self.position = new_position

        self.__evaluate_state()
        self.__evaluate_movement(clock)

        if self.state == Laser.LaserState.Recovery:
            self.width = (self.starting_width*(self.time_to_execute/LASER_ANTICIPATION_TIME))

    def render(self, display: "pygame.Surface"):
        if self.state == Laser.LaserState.Anticipation:
            new_color = (self.color[0]/2, self.color[1]/2, self.color[2]/2)
            pygame.draw.line(display, new_color, tuple(self.position), tuple(self.direction), self.width)
        elif self.state == Laser.LaserState.Attack:
            #pygame.draw.line(display, WHITE, tuple(self.position), tuple(self.direction), round(self.width+self.width*0.5))
            pygame.draw.line(display, self.color, tuple(self.position), tuple(self.direction), self.width)
        else:
            #pygame.draw.line(display, WHITE, tuple(self.position), tuple(self.direction), round(self.width+self.width*0.5))
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


    def __evaluate_movement(self, clock: "pygame.time.Clock"):

        if self.movement_types[0] == Laser.LaserMovement.Constant:
            pass #nothing to do here

        elif self.movement_types[0] == Laser.LaserMovement.AcceleratingStart and self.state == Laser.LaserState.Attack:
            if self.rotation_speed < self.max_rotation_speed:
                self.rotation_speed += (clock.get_time()/1000)*self.control_rotation_speed
            else:
                self.movement_types.pop(0)

        elif self.movement_types[0] == Laser.LaserMovement.DeceleratingEnd and self.state == Laser.LaserState.Attack and self.time_to_execute < LASER_ANTICIPATION_TIME*2:
            if self.rotation_speed > self.min_rotation_speed:
                self.rotation_speed -= (clock.get_time()/1000)*self.control_rotation_speed
            else:
                self.movement_types.pop(0)


    def set_type(self,
        move_types: list["Laser.LaserMovement"] = [LaserMovement.Constant],
        control_rotation_speed: number_types = 0, #pi/s
        max_rotation_speed: number_types = 0, #pi/s
        min_rotation_speed: number_types = 0, #pi/s
        )->None:
        if not isinstance(move_types, list):
            move_types = [move_types]
        if move_types[-1] != Laser.LaserMovement.Constant:
            move_types.append(Laser.LaserMovement.Constant)
        self.movement_types = move_types
        self.control_rotation_speed = control_rotation_speed
        self.max_rotation_speed = max_rotation_speed
        self.min_rotation_speed = min_rotation_speed



