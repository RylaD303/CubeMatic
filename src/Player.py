from typing import Union
from math import sin
from src.classes.Vector2D import Vector2D, number_types
from src.classes.GameObject import GameObject
import pygame


class Player(GameObject):
    """The Player Game object. Can move around"""
    def __init__(
        self,
        position: "Vector2D",
        speed: number_types,
        player_sprite: "pygame.Surface",
        width: number_types = 32,
        height: number_types = 32) -> "None":
        """Initialisation of Player object."""

        super().__init__(position)
        self.speed = speed
        self.__width = width
        self.__height = height
        self.sprite = pygame.transform.scale(player_sprite, (self.__width, self.__height))
        #self.sprite = player_sprite            #the sprite is 32 by 32 pixels anyway
        self.movement = Vector2D(0,0)
        self.rotation = 0

    def main(self, display, player_movement : list[bool]) -> None:
        """Draws the player on the screen.
        Recieve the player_movement to call on __move function."""
        self.__move(player_movement)
        display.blit(pygame.transform.rotate(self.sprite, self.rotation), tuple(self.position))

    def __move(self, player_movement : list[bool]):
        """Changes the Players position based on the player_movement vector.
        Vector scales with self.speed so palyer doesn't move faster diagonally"""

        if player_movement[0] :
            self.movement.x = -1
        if player_movement[1] :
            self.movement.x = 1
        if player_movement[2] :
            self.movement.y = -1
        if player_movement[3] :
            self.movement.y = 1

        movement_scaling = abs(self.movement)
        if movement_scaling > 0:
            self.rotation+=2
            self.rotation%=90
            self.position += self.speed*self.movement/movement_scaling

        self.movement.x = 0
        self.movement.y = 0




