import pygame
from src.Player import Player
from src.Teleport import Teleport
from src.Tiles import MapTile
from src.Bullet import Bullet
from src.GameValues import *

class CollisionHandler():
    def __call__(self, player: "Player", player_bullets: list["Bullet"], teleportation_device: "Teleport"):
        if player.position.x < START_OF_MAP.x+MAP_TILE_SIZE[0]:
            player.position.x = START_OF_MAP.x+MAP_TILE_SIZE[0]

        if player.position.x > END_OF_MAP.x-MAP_TILE_SIZE[0]-PLAYER_SCALE.x:
            player.position.x = END_OF_MAP.x-MAP_TILE_SIZE[0]-PLAYER_SCALE.x

        if player.position.y < START_OF_MAP.y+MAP_TILE_SIZE[1]:
            player.position.y = START_OF_MAP.y+MAP_TILE_SIZE[1]

        if player.position.y > END_OF_MAP.y-MAP_TILE_SIZE[1]-PLAYER_SCALE.y:
            player.position.y = END_OF_MAP.y-MAP_TILE_SIZE[1]-PLAYER_SCALE.y

        #Getting care of which bullets to remove
        bullets_to_remove: set[Bullet]= set()
        for bullet in player_bullets:
            if  bullet.position.x <=  START_OF_MAP.x+MAP_TILE_SIZE[0] or\
                bullet.position.x >= END_OF_MAP.x-MAP_TILE_SIZE[0] or\
                bullet.position.y <= START_OF_MAP.y+MAP_TILE_SIZE[1] or\
                bullet.position.y >= END_OF_MAP.y-MAP_TILE_SIZE[1]:

                bullets_to_remove.add(bullet)

        #Removing here, because we cannot change object while being iterated if any
        for bullet in bullets_to_remove:
            player_bullets.remove(bullet)

        if teleportation_device.active:
            if teleportation_device.position.x < START_OF_MAP.x+MAP_TILE_SIZE[0]:
                teleportation_device.movement.x = abs(teleportation_device.movement.x)

            if teleportation_device.position.x > END_OF_MAP.x-MAP_TILE_SIZE[0]:
                teleportation_device.movement.x = -abs(teleportation_device.movement.x)

            if teleportation_device.position.y < START_OF_MAP.y+MAP_TILE_SIZE[1]:
                teleportation_device.movement.y = abs(teleportation_device.movement.y)

            if teleportation_device.position.y > END_OF_MAP.y-MAP_TILE_SIZE[1]:
                teleportation_device.movement.y = -abs(teleportation_device.movement.y)
