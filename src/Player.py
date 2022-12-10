from typing import Union
from src.classes.Vector2D import Vector2D, number_types
from src.classes.GameObject import GameObject
import pygame


class Player(GameObject):
    def __init__(self, position : "Vector2D", speed : number_types = 5,
    width : number_types = 20, height : number_types = 20) -> "Player":

        super().__init__(position)
        self.speed = speed
        self.width = width
        self.height = height

    def main(self, display, player_movement : list[bool]) -> None:
        self.__move(player_movement)
        pygame.draw.rect(display, (0, 255, 0), (self.position.x, self.position.y, self.width, self.height))

    def __move(self, player_movement : list[bool]):
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


