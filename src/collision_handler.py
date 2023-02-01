import pygame
from src.game_objects.player import Player
from src.game_objects.teleport import Teleport
from src.game_objects.bullet import Bullet
from src.game_objects.laser import Laser
from src.game_objects.boss import Boss
from src.game_objects.effects import CircleEffect
from src.game_values import *


class CollisionHandler():
    """
    Handles the collision between all object on the screen.
    """
    def __call__(self,
                player: "Player",
                player_bullets: set["Bullet"],
                teleportation_device: "Teleport",
                boss: "Boss",
                boss_bullets: set["Bullet"],
                boss_lasers: set["Laser"],
                circle_effects: set["CircleEffect"]):

        player.check_out_of_bounds()

        #collects the player's bullets which need to be removed.
        players_bullets_to_remove: set[Bullet]= set()
        for bullet in player_bullets:
            if bullet.is_colliding_with(boss):
                bullet.invalidate()
                #todo!
            bullet.check_boundaries()
            if not bullet.is_valid():
                players_bullets_to_remove.add(bullet)


        #removes the player's bullets who are not valid.
        for bullet in players_bullets_to_remove:
            player_bullets.remove(bullet)

        #collects the boss' bullets which need to be removed.
        boss_bullets_to_remove: set[Bullet]= set()
        for bullet in boss_bullets:
            bullet.check_boundaries()
            if not bullet.is_valid():
                boss_bullets_to_remove.add(bullet)
                circle_effects.add(CircleEffect(bullet.position,BOSS_BULLET_SIZE*2))

        #removes the boss' bullets who are not valid.
        for bullet in boss_bullets_to_remove:
            boss_bullets.remove(bullet)

        if teleportation_device.active:
            teleportation_device.check_boundaries()

        effects_to_remove: set[Bullet]= set()
        for effect in circle_effects:
            if not effect.is_valid():
                effects_to_remove.add(effect)

        for effect in effects_to_remove:
            circle_effects.remove(effect)

