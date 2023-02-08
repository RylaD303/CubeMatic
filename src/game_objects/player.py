import os
import pygame
from src.classes.vector_2d import Vector2D, number_types
from src.classes.game_object import GameObject
from src.game_objects.bullet import Bullet
from src.game_values import *

pygame.mixer.init()
shoot_sound = pygame.mixer.Sound(os.path.join("src", "sounds", "player_fire.wav"))
shoot_sound.set_volume(0.4)

class Player(GameObject):
    """The Player Game object"""
    def __init__(
        self,
        position: "Vector2D",
        speed: number_types,
        player_sprite: "pygame.Surface",
        width: number_types = 64,
        height: number_types = 64) -> None:
        """
        Initialisation of Player object.

        Parameters:
            position -
                Vector2D starting position of the player object.
            speed -
                the players intended speed ingame.
            player_sprite -
                Surface object to be printed as the player's sprite.
            width -
                Intended width to scale the sprite with.
            height -
                Intended height to scale the sprite with.

        width and height should be equal.
        """

        super().__init__(position)
        self.speed = speed
        self.sprite =\
            pygame.transform.scale(player_sprite, (width, height))
        self.movement = Vector2D(0,0)
        self.rotation = 0
        self.fire_cooldown = 0
        self.radius = width/2

    def centre_position(self) -> "Vector2D":
        """
        Returns the player's current centre position.
        Scales with players size.
        """
        return self.position + PLAYER_SCALE/2

    def check_out_of_bounds(self):
        """
        Keeps player in map boundaries.
        """
        if self.position.x < START_OF_MAP.x:
            self.position.x = START_OF_MAP.x

        if self.position.x > END_OF_MAP.x-self.radius*2:
            self.position.x = END_OF_MAP.x-self.radius*2

        if self.position.y < START_OF_MAP.y:
            self.position.y = START_OF_MAP.y

        if self.position.y > END_OF_MAP.y-self.radius*2:
            self.position.y = END_OF_MAP.y-self.radius*2

    def main(self,
            player_movement : list[bool],
            clock: "pygame.time.Clock") -> None:
        """
        Handles player frame by frame
        Parameters:
            player_movement -
                list of 4 Bool for the 4 directions
                to call on _move function.
            clock -
                to evaluate last call of main so it can
                subtract from cooldown fire and scale player
                movement.
        """
        if self.fire_cooldown > 0:
            self.fire_cooldown -= clock.get_time()
        self._move(player_movement, clock)

    def _move(self,
              player_movement : list[bool],
              clock: "pygame.time.Clock")-> None:
        """
        Changes the Players position based on the player_movement
        vector.  Vector scales with self.speed so palyer doesn't
        move faster diagonally

        Parameters:
            player_movement -
                list of 4 Bool for the 4 directions
        """

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
            self.rotation+=700*clock.get_time()/SECOND
            self.rotation%=90
            self.position += self.speed\
                             * self.movement/movement_scaling\
                             * clock.get_time()/SECOND

        self.movement.x = 0
        self.movement.y = 0

    def fire(self,
            player_bullets: set["Bullet"],
            fire_to_position: "Vector2D") -> None:
        """
        Fires bullet to target location only (mouse position) if cooldown for firing
        is 0. When a bullet is fired the cooldown is reset.

        Parameters:
            player_bullets -
                set of bullets to add the supposedly fired bullet to
                so it can be handled on its own.

        """
        if self.fire_cooldown <=0:
            pygame.mixer.Sound.play(shoot_sound)
            bullet_to_fire = Bullet(self.centre_position(),
                                    fire_to_position,
                                    PLAYER_BULLET_COLOR,
                                    PLAYER_BULLET_SIZE,
                                    PLAYER_BULLET_SPEED)
            bullet_to_fire.set_slowdown_speed(PLAYER_BULLET_SLOWDOWN_SPEED)
            player_bullets.add(bullet_to_fire)
            self.fire_cooldown = PLAYER_SHOOT_COOLDOWN

    def render(self, display: "pygame.Surface") -> None:
        """
        Renders the player on a display.
        Scales with players rotation and sprites width

        Parameters:
            display - pygame.Surface
                to print the player on the surface.

        The function renders the player on a different position depending
        on its rotated sprite values. Because when a sprite rotates it
        increses its size to hold the new rotated imagine.
        """
        rotated_sprite = pygame.transform.rotate(self.sprite, self.rotation)
        position_to_print_on =Vector2D(\
            self.position.x\
            - (rotated_sprite.get_width() - self.sprite.get_width())/2,
            self.position.y\
            - (rotated_sprite.get_height() - self.sprite.get_height())/2)

        display.blit(rotated_sprite, tuple(position_to_print_on))
