from typing import Union
from src.classes.vector_2d import Vector2D, number_types
from src.classes.game_object import GameObject
from src.game_objects.player import Player
from src.game_values import *
import pygame

class Teleport(GameObject):
    def __init__(
        self,
        speed : number_types,
        radius: number_types = 4) -> "None":
        """Initialises teleportation device."""
        super().__init__(None)
        self.speed = speed
        self.radius = radius
        self.time_remaining = 0
        self.direction = None
        self.active = False


    def main(self, player: "Player", clock: "pygame.time.Clock"):
        """Handles teleportation device remaining time and teleportation."""
        if self.active:
            if self.time_remaining>MAX_HOLD_TIME/3*2:
                self.__move()
            self.time_remaining -= clock.get_time()
            if self.time_remaining<=0:
                self.teleport_player(player)

    def __move(self):
        """Moves the teleportation device by it's movement vector.
        Depending on the remaining time the movement will decrease"""
        if self.active:
            speed_scaling = (self.time_remaining - MAX_HOLD_TIME/3*2)/MAX_HOLD_TIME
            self.position += self.movement*(speed_scaling)

    def teleport_player(self, player: "Player"):
        """Deactivates the device and teleports the player to the target location"""
        player.position = self.position - Vector2D(player.width/2, player.height/2)
        self.deactivate()

    def render(self, display):
        """Renders the teleportation device on the screen if it is active."""
        if self.active:
            color = (255 - self.time_remaining*255/MAX_HOLD_TIME, 255, self.time_remaining*255/MAX_HOLD_TIME)
            pygame.draw.circle(display, color, (self.position.x, self.position.y), self.radius+2*((MAX_HOLD_TIME/self.time_remaining)/100))


    def activate(self, starting_position: "Vector2D", direction: "Vector2D",):
        self.starting_position = starting_position
        self.direction = direction
        self.position = starting_position
        self.time_remaining = MAX_HOLD_TIME
        if self.position == self.direction :
            self.direction+=1
        self.movement =  self.speed*(self.direction - self.position)/abs(self.direction - self.position)
        self.active = True

    def deactivate(self):
        self.active = False