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
        #ThreeSpiralShoot = 2
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
        self.speed = speed
        self.rotation = 0
        self.movement_pattern = None
        self.movement_variant = 0
        self.attack_sequence = Queue()
        self.current_attack_pattern = None
        self.time_to_execute = 0
        self.attack_cooldown = 0

    def centre_position(self) -> "Vector2D":
        return self.position + BOSS_SCALE/2

    def __choose_attack_sequence(self)-> None:
        #for attack in sample(following_attacks, 3):
        #    self.attack_sequence.put(attack)
        self.attack_sequence.put(Boss.FollowingAttackPattern.PlusLaser)
        self.attack_sequence.put(Boss.FollowingAttackPattern.WaveShots)
        self.attack_sequence.put(Boss.FollowingAttackPattern.PlusLaser)
        self.attack_sequence.put(Boss.FollowingAttackPattern.WaveShots)
        self.attack_sequence.put(Boss.FollowingAttackPattern.PlusLaser)

    def __pick_new_movement_pattern(self):
        self.movement_pattern = Boss.MovePattern.ParabolicMovement
        self.movement_variant = randint(1,2)

    def __evaluate_attack_pattern(self) -> None:
        if self.time_to_execute <= 0:
            if self.attack_sequence.empty():
                self.__choose_attack_sequence()
            self.current_attack_pattern = self.attack_sequence.get()
            self.attack_cooldown = 500
            self.time_to_execute = 8000 #ms
            self.__pick_new_movement_pattern()

    def __shoot_bullet_wave(self, player: "Player", boss_bullets: set["Bullet"]):
        self.attack_cooldown = BOSS_WAVE_SHOOT_COOLDOWN
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
        self.attack_cooldown = self.time_to_execute+1000
        lasers = [Laser(self.centre_position(), Vector2D(2,2), self.time_to_execute),
                Laser(self.centre_position(), Vector2D(-2,2), self.time_to_execute),
                Laser(self.centre_position(), Vector2D(2,-2), self.time_to_execute),
                Laser(self.centre_position(), Vector2D(-2,-2), self.time_to_execute)]
        for laser in lasers:
            laser.set_type_of_laser(
                [Laser.LaserMovement.AcceleratingStart, Laser.LaserMovement.DeceleratingEnd],
                 pi/6,
                 pi/3,
                 pi/9)
            boss_lasers.add(laser)

    def __execute_attack_pattern(self,
    player: "Player",
    boss_bullets: set["Bullet"],
    boss_lasers: set["Laser"],
    clock: "pygame.time.Clock") -> None:

        if self.current_attack_pattern == Boss.FollowingAttackPattern.WaveShots:
            if self.attack_cooldown <=0:
                if self.time_to_execute>BOSS_WAVE_SHOOT_COOLDOWN:
                    self.__shoot_bullet_wave(player, boss_bullets)
                else:
                    self.attack_cooldown = BOSS_WAVE_SHOOT_COOLDOWN

        elif self.current_attack_pattern == Boss.FollowingAttackPattern.PlusLaser:
            if self.attack_cooldown <=0:
                self.__add_plus_lasers(boss_lasers)



    def __evaluate_parabolic_movement(self):
        blend = 1 - self.time_to_execute/8000

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



    def __move(self):
        if self.movement_pattern == Boss.MovePattern.ParabolicMovement:
            self.__evaluate_parabolic_movement()


    def main(self, player: "Player", boss_bullets: list["Bullet"], boss_lasers: list["Laser"], clock: "pygame.time.Clock"):
        self.time_to_execute -= clock.get_time()
        self.attack_cooldown -= clock.get_time()
        self.__evaluate_attack_pattern()
        self.__move()
        self.__execute_attack_pattern(player, boss_bullets, boss_lasers, clock)


    def render(self, display: "pygame.Surface") -> None:
        if self.visible:
            rotated_sprite = pygame.transform.rotate(self.sprite, self.rotation)
            display.blit(\
                rotated_sprite,
                (self.position.x - (rotated_sprite.get_width() - self.sprite.get_width())/2,
                self.position.y - (rotated_sprite.get_height() - self.sprite.get_height())/2))



