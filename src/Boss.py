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


class Boss(GameObject):
    class FollowingAttackPattern(Enum):
        WaveShots = 1
        PlusLaser = 2
        EdgeLaser = 3
        SpiralShoot = 4

    class MovePattern(Enum):
        StandInMiddle = [1,{
            "time_to_execute": 10000,
            "time_for_one_laser_attack":8000,
            "cooldown_for_wave_shoot": BOSS_WAVE_SHOOT_COOLDOWN}]
        ParabolicMovement = [2,{
            "time_to_execute": 8000,
            "time_for_one_laser_attack":7000,
            "cooldown_for_wave_shoot": BOSS_WAVE_SHOOT_COOLDOWN}]
        #StandInMiddle = 2

        def get_time(self):
            return self.value[1]["time_to_execute"]
        def time_laser_attack(self):
            return self.value[1]["time_for_one_laser_attack"]
        def cooldown_for_wave_shoot(self):
            return self.value[1]["cooldown_for_wave_shoot"]

    following_attacks = list(FollowingAttackPattern)
    movement_patterns = list(MovePattern)

    def __init__(self,
        position: "Vector2D",
        speed: number_types,
        boss_sprite: "pygame.Surface",
        width: number_types = 64,
        height: number_types = 64) -> None:
        """Initialisation of Boss object."""

        super().__init__(position)
        #self.speed = speed
        #self.width = width
        #self.height = height
        self.sprite = pygame.transform.scale(boss_sprite, (width, height))
        self.width = width
        self.height = height
        self.speed = speed
        self.rotation = 0
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

    def __choose_attack_sequence(self)-> None:
        #for attack in sample(following_attacks, 3):
        #    self.attack_sequence.put(attack)
        self.attack_sequence.put(Boss.FollowingAttackPattern.SpiralShoot)
        self.attack_sequence.put(Boss.FollowingAttackPattern.SpiralShoot)
        self.attack_sequence.put(Boss.FollowingAttackPattern.EdgeLaser)
        self.attack_sequence.put(Boss.FollowingAttackPattern.EdgeLaser)
        self.attack_sequence.put(Boss.FollowingAttackPattern.PlusLaser)
        self.attack_sequence.put(Boss.FollowingAttackPattern.PlusLaser)
        self.attack_sequence.put(Boss.FollowingAttackPattern.WaveShots)
        self.attack_sequence.put(Boss.FollowingAttackPattern.WaveShots)

    def __pick_new_movement_pattern(self):
        self.movement_pattern = Boss.MovePattern.StandInMiddle
        self.movement_variant = 1#randint(1,2)

    def __evaluate_attack_pattern(self) -> None:
        if self.time_to_execute_pattern <= 0:
            if self.attack_sequence.empty():
                self.__choose_attack_sequence()
            self.current_attack_pattern = self.attack_sequence.get()
            self.attack_cooldown = 500
            self.angle_for_attack = None
            self.can_attack = True
            self.__pick_new_movement_pattern()
            self.time_to_execute_pattern = self.movement_pattern.get_time()

    def __shoot_bullet_wave(self, player: "Player", boss_bullets: set["Bullet"]):
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

    def __add_plus_lasers(self, boss_lasers: set["Laser"]):
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

    def __add_edge_laser(self, player: "Player", boss_lasers: set["Laser"]):
        self.attack_cooldown = self.time_to_execute_pattern+1000
        self.angle_for_attack = Vector2D(-1,0) if player.position.x > self.position.x else Vector2D(1,0)
        laser = Laser(self.centre_position(), self.angle_for_attack, self.movement_pattern.time_laser_attack())
        laser.set_type_of_laser(
            [Laser.LaserMovement.AcceleratingStart, Laser.LaserMovement.DeceleratingEnd],
            pi/2,
            pi,
            pi/9)
        boss_lasers.add(laser)

    def __shoot_spiral_bullets(self, boss_bullets: list["Bullet"], player: "Player"):
        if self.angle_for_attack is None:
            self.angle_for_attack = Vector2D(-1,0) if player.position.x > self.position.x else Vector2D(1,0)
        boss_bullets.add(
            Bullet(self.centre_position(),
            self.centre_position() + self.angle_for_attack,
            BOSS_ATTACK_COLOR,
            BOSS_BULLET_SIZE))
        self.angle_for_attack.angle_rotate(BOSS_SPIRAL_SHOOT_ATTACK_ROTATION)
        self.attack_cooldown = BOSS_SPIRAL_ATTACK_COOLDOWN


    def __execute_attack_pattern(self,
    player: "Player",
    boss_bullets: set["Bullet"],
    boss_lasers: set["Laser"],
    clock: "pygame.time.Clock") -> None:
        if not self.can_attack:
            return
        if self.current_attack_pattern == Boss.FollowingAttackPattern.WaveShots:
            if self.time_to_execute_pattern > self.movement_pattern.cooldown_for_wave_shoot():
                self.__shoot_bullet_wave(player, boss_bullets)

        elif self.current_attack_pattern == Boss.FollowingAttackPattern.PlusLaser:
            self.__add_plus_lasers(boss_lasers)


        elif self.current_attack_pattern == Boss.FollowingAttackPattern.EdgeLaser:
            self.__add_edge_laser(player, boss_lasers)

        elif self.current_attack_pattern == Boss.FollowingAttackPattern.SpiralShoot:
            self.__shoot_spiral_bullets(boss_bullets, player)


    def __evaluate_parabolic_movement(self):
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

    def __evaluate_stand_in_middle_movement(self):
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



    def __move(self):
        if self.movement_pattern == Boss.MovePattern.ParabolicMovement:
            self.__evaluate_parabolic_movement()
        if self.movement_pattern == Boss.MovePattern.StandInMiddle:
            self.__evaluate_stand_in_middle_movement()


    def main(self, player: "Player", boss_bullets: list["Bullet"], boss_lasers: list["Laser"], clock: "pygame.time.Clock"):
        self.time_to_execute_pattern -= clock.get_time()
        self.attack_cooldown -= clock.get_time()
        self.__evaluate_attack_pattern()
        self.__move()
        if self.attack_cooldown <=0:
            self.__execute_attack_pattern(player, boss_bullets, boss_lasers, clock)

    def render(self, display: "pygame.Surface") -> None:
        if self.visible:
            rotated_sprite = pygame.transform.rotate(self.sprite, self.rotation)
            display.blit(\
                rotated_sprite,
                (self.position.x - (rotated_sprite.get_width() - self.sprite.get_width())/2,
                self.position.y - (rotated_sprite.get_height() - self.sprite.get_height())/2))



