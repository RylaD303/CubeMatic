from src.classes.Vector2D import Vector2D, number_types
from src.classes.GameObject import GameObject
from src.Player import Player
from src.Bullet import Bullet
from src.GameValues import *

from random import sample
from queue import Queue
from enum import Enum
import pygame

class FollowingAttackPattern(Enum):
    FiveWaveShoot = 1
    ThreeSpiralShoot = 2
    PlusLaser = 3

class FollowingAttack(Enum):
    Laser = 1
    WaveShoot = 2
    SpiralShoot = 3

class MovePattern(Enum):
    CentralLine = 1
    StandInMiddle = 2
    ParabolicMovement = 3
    #CircularPattern
following_attacks = list(FollowingAttackPattern)


class Boss(GameObject):
    def __init__(self,
        position: "Vector2D",
        speed: number_types,
        player_sprite: "pygame.Surface",
        width: number_types = 64,
        height: number_types = 64) -> None:
        """Initialisation of Player object."""

        super().__init__(position)
        #self.speed = speed
        #self.width = width
        #self.height = height
        self.sprite = pygame.transform.scale(player_sprite, (width, height))
        self.rotation = 0
        self.attack_sequence = Queue()
        self.movement_pattern = Queue()
        self.current_attack_pattern = None
        self.time_to_execute = 0

    def __choose_attack_sequence(self):
        #for attack in sample(following_attacks, 3):
        #    self.attack_sequence.put(attack)
        self.attack_sequence.put(FollowingAttackPattern.FiveWaveShoot)

    def __evaluate_attack_pattern(self):
        if self.time_to_execute <= 0:
            self.current_attack_pattern = self.attack_sequence.get()
            self.time_to_execute = 6000 #ms

    def __execute_attack_pattern(self, player: "Player", boss_bullets: list["Bullet"], clock):
        #self.time_to_execute = 6000 #ms
        

