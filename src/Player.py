from src.classes.Vector2D import Vector2D, number_types
from src.classes.GameObject import GameObject
from src.Bullet import Bullet
from src.GameValues import *
import pygame


class Player(GameObject):
    """The Player Game object. Can move around"""
    def __init__(
        self,
        position: "Vector2D",
        speed: number_types,
        player_sprite: "pygame.Surface",
        width: number_types = 64,
        height: number_types = 64) -> None:
        """Initialisation of Player object."""

        super().__init__(position)
        self.speed = speed
        self.width = width
        self.height = height
        self.sprite = pygame.transform.scale(player_sprite, (self.width, self.height))
        self.movement = Vector2D(0,0)
        self.rotation = 0
        self.fire_cooldown = 0

    def main(self, player_movement : list[bool], clock: "pygame.time.Clock") -> None:
        """Handles player frame by frame
        Recieve the player_movement to call on __move function.
        Recieve clock to evaluate last call of main so it can subtract from cooldown fire."""
        if self.fire_cooldown > 0:
            self.fire_cooldown -= clock.get_time()
        self.__move(player_movement)

    def __move(self, player_movement : list[bool])-> None:
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
            self.rotation+=7
            self.rotation%=90
            self.position += self.speed*self.movement/movement_scaling

        self.movement.x = 0
        self.movement.y = 0
    def fire(self, player_bullets: list["Bullet"], fire_to_position: "Vector2D"):
        """Fires bullet to target location only if cooldown for firing is 0."""
        if self.fire_cooldown <=0:
            player_bullets.add(Bullet(self.position + PLAYER_SCALE/2, fire_to_position, PLAYER_BULLET_SPEED))
            self.fire_cooldown = PLAYER_SHOOT_COOLDOWN

    def render(self, display: "pygame.Surface"):
        rotated_sprite = pygame.transform.rotate(self.sprite, self.rotation)
        display.blit(\
            rotated_sprite,
            (self.position.x - (rotated_sprite.get_width() - self.sprite.get_width())/2,
            self.position.y - (rotated_sprite.get_height() - self.sprite.get_height())/2))




