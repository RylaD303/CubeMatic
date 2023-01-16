from src.classes.Vector2D import Vector2D, number_types
from src.classes.GameObject import GameObject
from src.GameValues import *

from random import sample
from queue import Queue
from enum import Enum
import pygame


class FollowingAttack(Enum):
    PlusLaser = 1
    WaveShoot = 2
    SpiralShoot = 3

class MovePattern(Enum):
    CentralLine = 1
    StandInMiddle = 2
    ParabolicMovement = 3
    #CircularPattern
following_attacks = list(FollowingAttack)


class Boss(GameObject):
    def __init__(self,
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
        self.rotation = 0
        self.attack_sequence = Queue()
        self.attacks_to_perform = Queue()
        self.movement_pattern = Queue()

    def __choose_attack_sequence(self):
        for attack in sample(following_attacks, 3):
            self.attack_sequence.append(attack)
