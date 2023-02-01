import pygame
from src.game_objects.player import Player
from src.game_objects.teleport import Teleport
from src.game_objects.bullet import Bullet
from src.game_objects.laser import Laser
from src.game_objects.boss import Boss
from src.game_objects.animations import CircleAnimation
from src.game_values import *


circle_animations: set["CircleAnimation"] = set()
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
                screen,
                clock):

        for circle_animation in circle_animations:
            circle_animation.render(screen)
        for circle_animation in circle_animations:
            circle_animation.main(clock)

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
                circle_animations.add(CircleAnimation(bullet.position,BOSS_BULLET_SIZE*2))

        #removes the boss' bullets who are not valid.
        for bullet in boss_bullets_to_remove:
            boss_bullets.remove(bullet)

        if teleportation_device.active:
            teleportation_device.check_boundaries()

        animations_to_remove: set[Bullet]= set()
        for animation in circle_animations:
            if not animation.is_valid():
                animations_to_remove.add(animation)

        for animation in animations_to_remove:
            circle_animations.remove(animation)

