from src.classes.Vector2D import Vector2D, number_types
from src.classes.GameObject import GameObject
from src.Player import Player
from src.Bullet import Bullet
from src.GameValues import *

from random import sample
from queue import Queue
from enum import Enum
from math import sin, cos, pi
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
        self.attack_cooldown = 0

    def __choose_attack_sequence(self)-> None:
        #for attack in sample(following_attacks, 3):
        #    self.attack_sequence.put(attack)
        self.attack_sequence.put(FollowingAttackPattern.FiveWaveShoot)

    def __evaluate_attack_pattern(self) -> None:
        if self.time_to_execute <= 0:
            self.current_attack_pattern = self.attack_sequence.get()
            self.time_to_execute = 6000 #ms

    def __execute_attack_pattern(self, player: "Player", boss_bullets: list["Bullet"], clock: "pygame.time.Clock") -> None:

        def create_bullet_with_angle(angle: number_types) -> "Bullet":
            bullet_direction = Vector2D(
                            player.position.x*cos(angle) - player.position.y*sin(angle),
                            player.position.x*sin(angle) + player.position.y*cos(angle))

            return Bullet(self.position, bullet_direction)


        #self.time_to_execute = 6000 #ms
        self.time_to_execute -= clock.get_time()
        self.attack_cooldown -= clock.get_time()
        self.__evaluate_attack_pattern()

        if self.current_attack_pattern == FollowingAttackPattern.FiveWaveShoot:
            if self.attack_cooldown <=0:
                self.attack_cooldown = 800 #ms
                angle = pi/9
                #central bullet
                boss_bullets.append(Bullet(self.position, player.position))
                for i in range(1,3):
                    boss_bullets.append(create_bullet_with_angle(i*angle))
                    boss_bullets.append(create_bullet_with_angle(-i*angle))


