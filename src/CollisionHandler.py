import pygame
from src.Player import Player
from src.Teleport import Teleport
from src.Bullet import Bullet
from src.GameValues import *

class CollisionHandler():
    def __call__(self, player: "Player", player_bullets: list["Bullet"], teleportation_device: "Teleport"):
        if player.position.x < START_OF_MAP.x:
            player.position.x = START_OF_MAP.x

        if player.position.x > END_OF_MAP.x-PLAYER_SCALE.x:
            player.position.x = END_OF_MAP.x-PLAYER_SCALE.x

        if player.position.y < START_OF_MAP.y:
            player.position.y = START_OF_MAP.y

        if player.position.y > END_OF_MAP.y-PLAYER_SCALE.y:
            player.position.y = END_OF_MAP.y-PLAYER_SCALE.y

        #Getting care of which bullets to remove
        bullets_to_remove: set[Bullet]= set()
        for bullet in player_bullets:
            if  bullet.position.x <=  START_OF_MAP.x or\
                bullet.position.x >= END_OF_MAP.x or\
                bullet.position.y <= START_OF_MAP.y or\
                bullet.position.y >= END_OF_MAP.y:

                bullets_to_remove.add(bullet)

        #Removing here, because we cannot change object while being iterated if any
        for bullet in bullets_to_remove:
            player_bullets.remove(bullet)

        if teleportation_device.active:
            if teleportation_device.position.x < START_OF_MAP.x:
                teleportation_device.movement.x = abs(teleportation_device.movement.x)

            if teleportation_device.position.x > END_OF_MAP.x:
                teleportation_device.movement.x = -abs(teleportation_device.movement.x)

            if teleportation_device.position.y < START_OF_MAP.y:
                teleportation_device.movement.y = abs(teleportation_device.movement.y)

            if teleportation_device.position.y > END_OF_MAP.y:
                teleportation_device.movement.y = -abs(teleportation_device.movement.y)
