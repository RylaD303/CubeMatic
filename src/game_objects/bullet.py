import pygame
from typing import Union

from src.classes.vector_2d import Vector2D, number_types
from src.classes.game_object import GameObject
from src.game_values import *

class Bullet(GameObject):
    """
    Bullet object that either the player or the boss fire.
    Handles its movement.
    """
    def __init__(
        self,
        starting_position: "Vector2D",
        direction: "Vector2D",
        color: tuple = (0, 255, 0),
        radius: number_types = 3,
        speed : number_types = 6) -> None:
        """
        Initialises the bullet.
        Parameters:
            starting position -
                the position of which the bullet was fired from;
            direction -
                the direction to which the bullet is fired;
            color -
                color of the bullet;
            radius -
                radius of the circle to be displayed for the bullet;
            speed -
                the bullets speed
        """
        super().__init__(starting_position)
        self.speed = speed
        self.direction = direction
        self.radius = radius
        self.color = color
        self.valid = True
        if self.position == self.direction :
            self.direction+=1

        self.movement = speed*(self.direction - self.position)\
                        / abs(self.direction - self.position)

    def invalidate(self):
        """
        Invalidates bullet so the collision handler can detect
        it should be removed.
        """
        self.valid = False

    def check_boundaries(self):
        """
        Checks if bullet is still in map boundaries.
        Invalidates bullet if it got out.
        """
        if  self.position.x <= START_OF_MAP.x\
            or self.position.x >= END_OF_MAP.x\
            or self.position.y <= START_OF_MAP.y\
            or self.position.y >= END_OF_MAP.y:
            self.invalidate()
    def is_colliding_with(self, other: "GameObject") -> bool:
        """
        Checks if the bullet is colliding with other game object.
        Should have radius of collision.
        Parameters:
            other -
                either player or boss objects.
        """
        distance = other.centre_position().distance_to(self.position)
        if other.radius + self.radius > distance:
            return True
        return False

    def is_valid(self):
        """Returns if the bullet got destroyed"""
        return self.valid

    def main(self, clock: "pygame.time.Clock") -> None:
        """ Handles the bullet frame by frame"""
        self.__move(clock)

    def __move(self, clock: "pygame.time.Clock") -> None:
        """
        Moves the bullet by it's movement vector,
        which is scaled by its speed and time passed.
        """
        self.position += self.movement*(clock.get_time()/1000)

    def render(self, display : "pygame.Surface"):
        """Displays bullet on screen"""
        pygame.draw.circle( display,
                            self.color,
                            (self.position.x, self.position.y),
                            self.radius)