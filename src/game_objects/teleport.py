from src.classes.vector_2d import Vector2D, number_types
from src.classes.game_object import GameObject
from src.game_objects.player import Player
from src.game_values import *
import pygame

class Teleport(GameObject):
    """
    Teleporation device which the player fires
    so he can teleport to it.
    """
    def __init__(
        self,
        speed : number_types,
        radius: number_types = 4) -> "None":
        """
        Initialises teleportation device.

        Parameters:
            speed -
                speed at which the object should be moving.
                (loses speed over time)
            radius -
                Radius of the rendered circle for the object.
        """
        super().__init__(None)
        self.speed = speed
        self.radius = radius
        self.time_remaining = 0
        self.direction = None
        self.active = False


    def main(self, player: "Player", clock: "pygame.time.Clock") -> None:
        """
        Handles teleportation device remaining time and teleportation.

        Parameters:
            player -
                to change players location on teleport
            clock -
                to change remaining cooldowns.
        """
        if self.active:
            if self.time_remaining>MAX_HOLD_TIME/3*2:
                self.__move(clock)
            self.time_remaining -= clock.get_time()
            if self.time_remaining<=0:
                self.teleport_player(player)

    def check_boundaries(self):
        if self.position.x < START_OF_MAP.x:
            self.movement.x = abs(self.movement.x)

        if self.position.x > END_OF_MAP.x:
            self.movement.x = -abs(self.movement.x)

        if self.position.y < START_OF_MAP.y:
            self.movement.y = abs(self.movement.y)

        if self.position.y > END_OF_MAP.y:
            self.movement.y = -abs(self.movement.y)

    def __move(self, clock: "pygame.time.Clock"):
        """
        Moves the teleportation device by it's movement vector.
        Depending on the remaining time the movement will decrease
        """
        if self.active:
            speed_scaling = (self.time_remaining - MAX_HOLD_TIME/3*2)\
                            / MAX_HOLD_TIME
            self.position += self.movement\
                             * (speed_scaling)\
                             * clock.get_time()/SECOND

    def teleport_player(self, player: "Player"):
        """
        Deactivates the device and teleports the player to the
        target location.

        Parameters:
            player -
                to change location on teleport.
        """
        player.position =\
            self.position - Vector2D(player.sprite.get_width()/2,\
                                                   player.sprite.get_height()/2)
        self.deactivate()

    def render(self, display):
        """
        Renders the teleportation device on the screen if it is active.

        Parameters:
            display -
                Surface on which to print the device.
        """
        if self.active:
            color = (255 - self.time_remaining*255/MAX_HOLD_TIME,
                    255,
                    self.time_remaining*255/MAX_HOLD_TIME)
            pygame.draw.circle(display,
                               color,
                               (self.position.x, self.position.y),
                               self.radius\
                               + 2*((MAX_HOLD_TIME/self.time_remaining)/100))


    def activate(self, starting_position: "Vector2D", direction: "Vector2D"):
        """
        Activates the teleportation device, shoots it in
        a direction and sets the cooldown timer.

        Parameters:
            starting_position -
                where the teleportation device shoots from.
            direction -
                to which direction should it shoot to.
        """
        self.starting_position = starting_position
        self.direction = direction
        self.position = starting_position
        self.time_remaining = MAX_HOLD_TIME
        if self.position == self.direction :
            self.direction+=1
        self.movement =  self.speed*(self.direction - self.position)/abs(self.direction - self.position)
        self.active = True

    def deactivate(self):
        """
        Deactivates the teleportation device.
        It is not rendered when unactive and won't teleport player.
        """
        self.active = False