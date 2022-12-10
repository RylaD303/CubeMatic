from typing import Union
from src.classes.Vector2D import Vector2D, number_types
from src.classes.GameObject import GameObject
import pygame


class Player(GameObject):
    """The Player Game object. Can move around"""
    def __init__(self, position : "Vector2D", speed : number_types = 5,
    width : number_types = 20, height : number_types = 20) -> "Player":
        """Initialisation of Player object."""
        super().__init__(position)
        self.speed = speed
        self.width = width
        self.height = height

    def main(self, display, player_movement : list[bool]) -> None:
        """Draws the player on the screen.
        Recieve the player_movement to call on __move function."""
        self.__move(player_movement)
        pygame.draw.rect(display, (0, 255, 0), (self.position.x, self.position.y, self.width, self.height))

    def __move(self, player_movement : list[bool]):
        """Changes the Players position based on the player_movement vector.
        Vector scales with self.speed so palyer doesn't move faster diagonally"""
        movement = Vector2D(0,0)
        if player_movement[0] :
            movement.x -= 1
        if player_movement[1] :
            movement.x += 1
        if player_movement[2] :
            movement.y -= 1
        if player_movement[3] :
            movement.y += 1

        scaling = abs(movement)
        if scaling > 0:
            self.position += self.speed*movement/scaling


