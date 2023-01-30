import pygame

from src.classes.vector_2d import Vector2D, number_types
from src.classes.game_object import GameObject


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
        radius: number_types = 2,
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
                the bullets speed"""
        super().__init__(starting_position)
        self.speed = speed
        self.direction = direction
        self.radius = radius
        self.color = color
        if self.position == self.direction :
            self.direction+=1

        self.movement = speed*(self.direction - self.position)\
                        / abs(self.direction - self.position)

    def main(self) -> None:
        """Handles the bullet frame by frame"""
        self.__move()

    def __move(self) -> None:
        """
        Moves the bullet by it's movement vector,
        which is scaled by its speed
        """
        self.position += self.movement

    def render(self, display : "pygame.Surface"):
        """Displays bullet on screen"""
        pygame.draw.circle( display,
                            self.color,
                            (self.position.x, self.position.y),
                            self.radius)
