from src.classes.Vector2D import Vector2D, number_types
from src.classes.GameObject import GameObject
from src.Player import Player
from src.Bullet import Bullet
from src.GameValues import *
from src.Laser import Laser




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
        self.__choose_attack_sequence()

    def __choose_attack_sequence(self)-> None:
        #for attack in sample(following_attacks, 3):
        #    self.attack_sequence.put(attack)
        self.attack_sequence.put(FollowingAttackPattern.FiveWaveShoot)
        self.attack_sequence.put(FollowingAttackPattern.PlusLaser)
        self.attack_sequence.put(FollowingAttackPattern.FiveWaveShoot)
        self.attack_sequence.put(FollowingAttackPattern.PlusLaser)
        self.attack_sequence.put(FollowingAttackPattern.FiveWaveShoot)
        self.attack_sequence.put(FollowingAttackPattern.PlusLaser)

    def __evaluate_attack_pattern(self) -> None:
        if self.time_to_execute <= 0:
            self.current_attack_pattern = self.attack_sequence.get()
            self.attack_cooldown = 0
            self.time_to_execute = 6000 #ms

    def __execute_attack_pattern(self, player: "Player", boss_bullets: list["Bullet"], boss_lasers: list["Laser"], clock: "pygame.time.Clock") -> None:

        self.time_to_execute -= clock.get_time()
        self.attack_cooldown -= clock.get_time()
        self.__evaluate_attack_pattern()

        if self.current_attack_pattern == FollowingAttackPattern.FiveWaveShoot:
            if self.attack_cooldown <=0:
                self.attack_cooldown = 800 #ms
                angle = pi/9
                #central bullet
                boss_bullets.append(Bullet(self.position, player.position))
                #side nnullets
                for i in range(1,3):
                    boss_bullets.append(Bullet(self.position, player.position.new_angle_rotate(i*angle)))
                    boss_bullets.append(Bullet(self.position, player.position.new_angle_rotate(-i*angle)))
        elif self.current_attack_pattern == FollowingAttackPattern.PlusLaser:
            if self.attack_cooldown <=0:
                self.attack_cooldown = self.time_to_execute+1000
                boss_lasers.append([
                    Laser(self.position, Vector2D(2,2), self.time_to_execute),
                    Laser(self.position, Vector2D(-2,2), self.time_to_execute),
                    Laser(self.position, Vector2D(2,-2), self.time_to_execute),
                    Laser(self.position, Vector2D(-2,-2), self.time_to_execute),
                ])



    def render_self(self, display: "pygame.Surface") -> None:
        if self.visible:
            rotated_sprite = pygame.transform.rotate(self.sprite, self.rotation)
            display.blit(\
                rotated_sprite,
                (self.position.x - (rotated_sprite.get_width() - self.sprite.get_width())/2,
                self.position.y - (rotated_sprite.get_height() - self.sprite.get_height())/2))



