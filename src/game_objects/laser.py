from src.game_values import *
from src.classes.vector_2d import Vector2D, number_types
from src.classes.game_object import GameObject
import pygame
from enum import Enum

WHITE = (255, 255 ,255)
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


class Laser(GameObject):
    """
    Laser object for the boss attacks.

    Handles own movement and chagne of states.
    """

    def __init__(self,
        begin_point: "Vector2D",
        direction: "Vector2D",
        time: number_types, #ms
        width: number_types = 10,
        color: tuple = (255, 0, 0))-> None:
        """
        Initialises the Laser object.

        Parameters:
            begin_point -
                Starting point of the laser.
            direction -
                Direction of the laser.
            time -
                time for the laser to live.
            width -
                width of the laser.
            color -
                color with which the laser will be rendered.
        """
        super().__init__(begin_point)
        self.direction = (direction/abs(direction))*(LASER_LENGTH**2)
        self.width = width
        self.starting_width = width
        self.color = color
        self.state = LaserState.Anticipation
        self.movement_types = [LaserMovement.Constant]
        self.rotation_speed = 0
        self.cooldown = LASER_ANTICIPATION_TIME
        self.time_to_execute = time


    def main(self,
            clock: "pygame.time.Clock",
            new_position: "Vector2D" = None):
        """
        Handles main part of the laser - movement, state evaluation,
        time left to execute.

        Parameters:
            clock -
                to evaluate time left to live.
            new_position -
                the new position at frame of which the laser should be
                comnig from. If not given one, the laser stays in one
                place.
        """
        self.cooldown -= clock.get_time()
        self.time_to_execute -= clock.get_time()
        self.direction.angle_rotate(self.rotation_speed*clock.get_time()/1000)
        if new_position:
            self.position = new_position

        self.__evaluate_state()
        self.__evaluate_movement(clock)

        if self.state == LaserState.Recovery:
            self.width = (self.starting_width\
                        * (self.time_to_execute/LASER_ANTICIPATION_TIME))

    def render(self, display: "pygame.Surface"):
        """
        Renders the laser on a display.
        The function renders the laser in a different ways depending
        on its current state. If the state is anticipation then the
        laser renders as slightly faded self. If the state is attack,
        then the laser pritns as it should be, and if it is in recovery,
        the laser contracts.
        Parameters:
            display - pygame.Surface
                to print the player on the surface.
        """
        if self.state == LaserState.Anticipation:
            new_color = (self.color[0]/2, self.color[1]/2, self.color[2]/2)
            pygame.draw.line(display,
                            new_color,
                            tuple(self.position),
                            tuple(self.direction),
                            round(self.width))

        elif self.state == LaserState.Attack:
            pygame.draw.line(display,
                            self.color,
                            tuple(self.position),
                            tuple(self.direction),
                            self.width)
            # pygame.draw.line(display,
            #                 WHITE,
            #                 tuple(self.position),
            #                 tuple(self.direction),
            #                 round(self.width/3))
        else:
            pygame.draw.line(display,
                            WHITE,
                            tuple(self.position),
                            tuple(self.direction),
                            round(self.width))

    def __evaluate_state(self):
        """
        Evaluates the current statec of the laser.
        States are in the order:
        Anticipation,
        Attack,
        Recovery.
        """
        if self.cooldown<=0:
            if self.state == LaserState.Anticipation:
                self.state = LaserState.Attack
                self.cooldown = self.time_to_execute-LASER_ANTICIPATION_TIME
            elif self.state == LaserState.Attack:
                self.state = LaserState.Recovery
                self.time_to_execute = LASER_ANTICIPATION_TIME
                self.cooldown = LASER_ANTICIPATION_TIME


    def __evaluate_movement(self, clock: "pygame.time.Clock"):
        """
        Evaluates the movement of the laser, given the movement_types
        it was given.

        Parameters:
            clock -
                to set cooldowns with.
        """
        if self.movement_types[0] == LaserMovement.Constant:
            pass #nothing to do here

        elif self.movement_types[0] == LaserMovement.AcceleratingStart\
             and self.state == LaserState.Attack:

            if self.rotation_speed < self.max_rotation_speed:
                self.rotation_speed +=\
                    (clock.get_time()/1000)*self.control_rotation_speed
            else:
                self.movement_types.pop(0)

        elif self.movement_types[0] == LaserMovement.DeceleratingEnd\
            and self.state == LaserState.Attack\
            and self.time_to_execute < LASER_ANTICIPATION_TIME*2:

            if self.rotation_speed > self.min_rotation_speed:
                self.rotation_speed -=\
                    (clock.get_time()/1000)*self.control_rotation_speed
            else:
                self.movement_types.pop(0)


    def set_type(self,
        move_types: list["LaserMovement"] = [LaserMovement.Constant],
        control_rotation_speed: number_types = 0, #pi/s
        max_rotation_speed: number_types = 0, #pi/s
        min_rotation_speed: number_types = 0, #pi/s
        )->None:
        """
        Sets the type of movement for the laser.
        All speeds calculated with pi/s.
        Parameters:
            move_types -
                list of laser type movements.
            control_rotation_speed -
                at what speed should the laser accelerate/decelerate
            max_rotation_speed -
                the max speed the laser can reach.
            min_rotation_speed -
                the minimum speed at which the laser is rotating.
        """
        if not isinstance(move_types, list):
            move_types = [move_types]
        if move_types[-1] != LaserMovement.Constant:
            move_types.append(LaserMovement.Constant)
        self.movement_types = move_types
        self.control_rotation_speed = control_rotation_speed
        self.max_rotation_speed = max_rotation_speed
        self.min_rotation_speed = min_rotation_speed



