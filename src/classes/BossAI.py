from random import sample, randint
from queue import Queue
from enum import Enum
from math import sin, cos, pi, sqrt
import pygame



from src.classes.Vector2D import Vector2D, number_types
from src.classes.GameObject import GameObject
from src.Player import Player
from src.Bullet import Bullet
from src.GameValues import *
from src.Laser import Laser


class BossAI(GameObject):
    class FollowingAttackPattern(Enum):
        WaveShots = 1
        PlusLaser = 2
        EdgeLaser = 3
        SpiralShoot = 4

    class MovePattern(Enum):
        StandInMiddle = [1,{
            "time_to_execute": 10000,
            "time_for_one_laser_attack":7000,
            "cooldown_for_wave_shoot": BOSS_WAVE_SHOOT_COOLDOWN}]
        ParabolicMovement = [2,{
            "time_to_execute": 8000,
            "time_for_one_laser_attack":7000,
            "cooldown_for_wave_shoot": BOSS_WAVE_SHOOT_COOLDOWN}]
        #StandInMiddle = 2

        def get_time(self) -> number_types:
            return self.value[1]["time_to_execute"]
        def time_laser_attack(self)  -> number_types:
            return self.value[1]["time_for_one_laser_attack"]
        def cooldown_for_wave_shoot(self)  -> number_types:
            return self.value[1]["cooldown_for_wave_shoot"]

    following_attacks = list(FollowingAttackPattern)
    movement_patterns = list(MovePattern)

    def __init__(self) -> None:
        """Initialisation of Boss object."""

        super().__init__(Vector2D(0,0))
        #self.speed = speed
        #self.width = width
        #self.height = height
        self.movement_pattern = None
        self.movement_variant = 0
        self.attack_sequence = Queue()
        self.current_attack_pattern = None
        self.attack_cooldown = 0
        self.angle_for_attack = None
        self.time_to_execute_pattern = 0
        self.can_attack = False

    def centre_position(self) -> "Vector2D":
        return self.position + BOSS_SCALE/2


    def _pick_new_movement_pattern(self)  -> None:
        self.movement_pattern = BossAI.MovePattern.StandInMiddle
        self.movement_variant = randint(1,4)

    def _shoot_bullet_wave(self, player: "Player", boss_bullets: set["Bullet"])  -> None:
        self.attack_cooldown = self.movement_pattern.cooldown_for_wave_shoot()
        #central bullet
        boss_bullets.add(
            Bullet(self.centre_position(),
            player.position,
            BOSS_ATTACK_COLOR,
            BOSS_BULLET_SIZE))
        #side nnullets
        for i in range(1,3):
            bullet1 = Bullet(
                self.centre_position(),
                player.position,
                BOSS_ATTACK_COLOR,
                BOSS_BULLET_SIZE)
            bullet1.movement.angle_rotate(i*BOSS_WAVE_SHOOT_ANGLE)
            boss_bullets.add(bullet1)
            bullet2 = Bullet(
                self.centre_position(),
                player.position,
                BOSS_ATTACK_COLOR,
                BOSS_BULLET_SIZE)
            bullet2.movement.angle_rotate(-i*BOSS_WAVE_SHOOT_ANGLE)
            boss_bullets.add(bullet2)

    def _add_plus_lasers(self, boss_lasers: set["Laser"])  -> None:
        self.attack_cooldown = self.movement_pattern.time_laser_attack()
        lasers = [Laser(self.centre_position(), Vector2D(2,2),self.movement_pattern.time_laser_attack()),
                Laser(self.centre_position(), Vector2D(-2,2), self.movement_pattern.time_laser_attack()),
                Laser(self.centre_position(), Vector2D(2,-2), self.movement_pattern.time_laser_attack()),
                Laser(self.centre_position(), Vector2D(-2,-2), self.movement_pattern.time_laser_attack())]
        for laser in lasers:
            laser.set_type_of_laser(
                [Laser.LaserMovement.AcceleratingStart, Laser.LaserMovement.DeceleratingEnd],
                 pi/4,
                 pi/2,
                 pi/9)
            boss_lasers.add(laser)

    def _add_edge_laser(self, player: "Player", boss_lasers: set["Laser"])  -> None:
        self.attack_cooldown = self.time_to_execute_pattern+1000
        self.angle_for_attack = Vector2D(-1,0) if player.position.x > self.position.x else Vector2D(1,0)
        laser = Laser(self.centre_position(),
                      self.angle_for_attack,
                      self.movement_pattern.time_laser_attack())
        laser.set_type_of_laser(
            [Laser.LaserMovement.AcceleratingStart, Laser.LaserMovement.DeceleratingEnd],
            pi/2,
            pi,
            pi/9)
        boss_lasers.add(laser)
        if self.movement_pattern == BossAI.MovePattern.StandInMiddle:
            laser2 = Laser(self.centre_position(),
                           self.angle_for_attack,
                           self.movement_pattern.time_laser_attack())
            laser2.set_type_of_laser(
                [Laser.LaserMovement.AcceleratingStart, Laser.LaserMovement.DeceleratingEnd],
                pi/2,
                pi,
                pi/9)
            laser2.direction.angle_rotate(pi)
            boss_lasers.add(laser2)

    def _shoot_spiral_bullets(self, boss_bullets: list["Bullet"], player: "Player")  -> None:
        if self.angle_for_attack is None:
            self.angle_for_attack = Vector2D(-1,0) if player.position.x > self.position.x else Vector2D(1,0)
        boss_bullets.add(
            Bullet(self.centre_position(),
            self.centre_position() + self.angle_for_attack,
            BOSS_ATTACK_COLOR,
            BOSS_BULLET_SIZE))
        if self.movement_pattern == BossAI.MovePattern.StandInMiddle:
            boss_bullets.add(
                Bullet(self.centre_position(),
                self.centre_position() + self.angle_for_attack.angle_rotated(pi),
                BOSS_ATTACK_COLOR,
                BOSS_BULLET_SIZE))
        self.angle_for_attack.angle_rotate(BOSS_SPIRAL_SHOOT_ATTACK_ROTATION)
        self.attack_cooldown = BOSS_SPIRAL_ATTACK_COOLDOWN


    def _evaluate_parabolic_movement(self) -> None:
        blend = 1 - self.time_to_execute_pattern/self.movement_pattern.get_time()
        if blend<0.1 or blend>0.9:
            self.can_attack = False
        else:
            self.can_attack = True
        #evaluating the x axis positin for the elipse (they are the same for both centres)
        x = blend*(BOSS_UPPER_CENTRE_OF_ELIPSE.x + BOSS_ELIPSE_WIDTH)
        a2 = BOSS_ELIPSE_WIDTH**2
        elx = ((x - BOSS_UPPER_CENTRE_OF_ELIPSE.x)**2)/a2

        if self.movement_variant == 1:
            #evaluating the y length of the elipse so we can get the position
            b2 = BOSS_ELIPSE_HEIGHT**2
            y = sqrt((1 - elx)*b2) - BOSS_UPPER_CENTRE_OF_ELIPSE.y
            self.position = Vector2D(x, y)

        if self.movement_variant == 2:
            #evaluating the y length of the elipse so we can get the position
            b2 = BOSS_ELIPSE_HEIGHT**2
            y = sqrt((1 - elx)*b2) + BOSS_LOWER_CENTRE_OF_ELIPSE.y

            #getting the mirror image of y, so we can invert the half elipse
            #and moving it to the correct position
            y = -y + 2*BOSS_LOWER_CENTRE_OF_ELIPSE.y
            self.position = Vector2D(x, y)

    def _evaluate_stand_in_middle_movement(self) -> None:
        blend = self.time_to_execute_pattern/self.movement_pattern.get_time()
        if blend<=0.2 or blend>=0.8:
            self.can_attack = False
            current_blend = blend*5 if blend<=0.2 else (blend - 0.8)*5 + 1
            current_blend /= 2
            if self.movement_variant in [2,4]:
                current_blend = 1 - current_blend # opposite
            if self.movement_variant in [1,2]:
                self.position = current_blend*Vector2D(0,CENTRE_OF_MAP.y) +\
                                (1 - current_blend)*Vector2D(CENTRE_OF_MAP.x*2,CENTRE_OF_MAP.y)
            else:
                self.position = current_blend*Vector2D(CENTRE_OF_MAP.x,0) +\
                                (1 - current_blend)*Vector2D(CENTRE_OF_MAP.x,CENTRE_OF_MAP.y*2)
        else:
            self.can_attack = True
            self.position = CENTRE_OF_MAP