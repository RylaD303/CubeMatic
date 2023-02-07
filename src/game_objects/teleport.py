import pygame
from src.classes.vector_2d import Vector2D, number_types
from src.classes.game_object import GameObject
from src.game_objects.player import Player
from src.game_objects.effects import CircleEffect
from src.game_objects.effects import CircleEffect
from src.game_values import *

pygame.mixer.init()
sound = pygame.mixer.Sound("src/sounds/teleport_player.wav")
sound.set_volume(0.4)

pygame.mixer.init()
teleportation_sound = pygame.mixer.Sound("src/sounds/teleport_player.wav")
teleportation_sound.set_volume(0.4)
class Teleport(GameObject):
    """
    Teleporation device which the player fires
    so he can teleport to it.
    """
    def __init__(
        self,
        speed: float,
        sprite : "pygame.Surface",
        scale: "Vector2D") -> "None":
        """
        Initialises teleportation device.

        Parameters:
            speed -
                speed at which the object should be moving.
                (loses speed over time)
            sprite -
                sprite to render for teleport.
            scale -
                scale of sprite
        """
        super().__init__(None)
        self.sprite =\
            pygame.transform.scale(sprite, (scale.x, scale.y))
        self.rotation = 0
        self.speed = speed
        self.time_remaining = 0
        self.direction = None
        self.active = False


    def main(self,
            player: "Player",
            clock: "pygame.time.Clock",
            circle_effects: set["CircleEffect"]) -> None:
        """
        Handles teleportation device remaining time and teleportation.

        Parameters:
            player -
                to change players location on teleport
            clock -
                to change remaining cooldowns.
        """
        if self.active:
            self.rotation = player.rotation
            if self.time_remaining>MAX_HOLD_TIME/3*2:
                self.__move(clock)
            self.time_remaining -= clock.get_time()
            if self.time_remaining<=0:
                self.teleport_player(player, circle_effects)

    def check_boundaries(self):
        if self.position.x < START_OF_MAP.x:
            self.movement.x = abs(self.movement.x)

        if self.position.x > END_OF_MAP.x - self.sprite.get_width():
            self.movement.x = -abs(self.movement.x)

        if self.position.y < START_OF_MAP.y:
            self.movement.y = abs(self.movement.y)

        if self.position.y > END_OF_MAP.y - self.sprite.get_height():
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

    def teleport_player(self,
                        player: "Player",
                        circle_effects: set["CircleEffect"]):
        """
        Deactivates the device and teleports the player to the
        target location.

        Parameters:
            player -
                to change location on teleport.
        """
        circle_effects.add(CircleEffect(
            player.centre_position(),
            player.radius*1.4
        ))
        pygame.mixer.Sound.play(teleportation_sound)
        player.position = self.position
        self.deactivate()
        circle_effects.add(CircleEffect(
            player.centre_position(),
            player.radius*1.4
        ))
    def render(self, display):
        """
        Renders the teleportation device on the screen if it is active.

        Parameters:
            display -
                Surface on which to print the device.
        """
        if self.active:
            rotated_sprite = pygame.transform.rotate(self.sprite, self.rotation)
            position_to_print_on =Vector2D(\
                self.position.x\
                - (rotated_sprite.get_width() - self.sprite.get_width())/2,
                self.position.y\
                - (rotated_sprite.get_height() - self.sprite.get_height())/2)

            display.blit(rotated_sprite, tuple(position_to_print_on))


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
