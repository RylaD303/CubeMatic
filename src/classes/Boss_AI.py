from random import randint
from queue import Queue
from enum import Enum
from math import pi, sqrt



from src.classes.vector_2d import Vector2D, number_types
from src.classes.game_object import GameObject
from src.game_objects.player import Player
from src.game_objects.bullet import Bullet
from src.game_values import *
from src.game_objects.laser import Laser


class BossAI(GameObject):
    """
    BossAI object.
    Handles the movement patterns and the attack patterns of
    the Boss. Value of enums is ID.
    """
    class FollowingAttackPattern(Enum):
        """
        """
        WaveShots = 1
        PlusLaser = 2
        EdgeLaser = 3
        SpiralShoot = 4

    class MovePattern(Enum):
        """
        Enum for state of movement pattern of the boss.
        First value of Enum is ID.
        Second value is dict describing how attack patterns
        should act.
        """

        StandInMiddle = [1, {"time_to_execute": 10000,
                             "time_for_one_laser_attack":8000,
                             "cooldown_for_wave_shoot":
                             BOSS_WAVE_SHOOT_COOLDOWN}]
        ParabolicMovement = [2, {"time_to_execute": 8000,
                                 "time_for_one_laser_attack":6800,
                                 "cooldown_for_wave_shoot":
                                 BOSS_WAVE_SHOOT_COOLDOWN}]
        #StandInMiddle = 2

        def get_time(self) -> number_types:
            """
            Returns the enums corresponding time to
            execute movement patter
            """
            return self.value[1]["time_to_execute"]
        def time_laser_attack(self)  -> number_types:
            """
            Returns the enums corresponding time to
            execute laser attack pattern
            """
            return self.value[1]["time_for_one_laser_attack"]
        def cooldown_for_wave_shoot(self)  -> number_types:
            """
            Returns the enums corresponding cooldown for
            wave shoot attack pattern
            """
            return self.value[1]["cooldown_for_wave_shoot"]

    following_attacks = list(FollowingAttackPattern)
    movement_patterns = list(MovePattern)

    def __init__(self) -> None:
        """
        Initialisation of BossAI object.
        Has:
        current_movement_pattern -
            current movement pattern execution;
        movement_variant -
            variant of the movement pattern to execute;
        attack_sequence -
            Queue of attack patterns to execute,
            refills with new patterns once empty;
        current_attack_pattern -
            current attack pattern execution;
        attack_cooldown -
            current attacks cooldown in ms,
            once the cooldown is 0, new attack will be executed
            and timer will be set for next attack;
        angle_for_attack -
            current attacks angle to shoot. Mainly used for laser;

        can_attack -
            bool variable that indicates whether the boss can execute
            an attack or not. Mainly controlled by the movement
            patterns;

        time_to_execute_pattern -
            time left to execute the current movement pattern.
        """

        super().__init__(Vector2D(0,0))
        #self.speed = speed
        #self.width = width
        #self.height = height
        self.current_movement_pattern = None
        self.movement_variant = 0
        self.attack_sequence = Queue()
        self.current_attack_pattern = None
        self.attack_cooldown = 0
        self.angle_for_attack = None
        self.can_attack = False
        self.time_to_execute_pattern = 0

    def centre_position(self) -> "Vector2D":
        """
        Returns the centre position of the Boss,
        depending on its scale.

        return_t: Vector2D
        """
        return self.position + BOSS_SCALE/2

    def _pick_new_movement_pattern(self)  -> None:
        """todo!"""
        self.current_movement_pattern = BossAI.MovePattern.StandInMiddle
        self.movement_variant = randint(1,4)

    def _shoot_bullet_wave(self, player: "Player",
                           boss_bullets: set["Bullet"])  -> None:
        """
        Executes attack WAVESHOOT:
        Shoots a wave of five bullets towards the player.
        Parameters:
        player:
            for position of player
        Set of bullets:
            to add the bullets so they can be handled
        """
        self.attack_cooldown =\
            self.current_movement_pattern.cooldown_for_wave_shoot()
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
        """
        Executes the plus laser attack pattern.
        Adds four lasers pointing to the main diagonals
        and sets them to accelerate in the beggining and
        decelerate at the end.
        Parameters:
        Set of boss lasers:
            to add the lasers so they can be handled.
        """
        self.attack_cooldown =\
            self.current_movement_pattern.time_laser_attack()
        plus_laser_directions = [Vector2D(2,2),
                                 Vector2D(-2,2),
                                 Vector2D(2,-2),
                                 Vector2D(-2,-2)]
        lasers = [Laser(self.centre_position(),
                        direction,
                        self.current_movement_pattern.time_laser_attack())
                    for direction in plus_laser_directions]
        plus_laser_behaviour = [Laser.LaserMovement.AcceleratingStart,
                                Laser.LaserMovement.DeceleratingEnd]
        for laser in lasers:
            laser.set_type( plus_laser_behaviour, pi/4, pi/2, pi/9)
            boss_lasers.add(laser)

    def _add_edge_laser(self, player: "Player",
                        boss_lasers: set["Laser"])  -> None:
        """
        Executes the edge laser attack pattern.
        Adds one laser pointing away from the player.
        Sets the laser to fast speed, sets it to
        accelerate in the beggining and decelerate
        at the end.

        In case of Stand in middle movement pattern
        adds a second pattern so it is not so easy
        to dodge.

        Parameters:
        player:
            to know the players position, so it can
            set the laser's direction away from player.
        set of lasers:
            to add them to the set os they can be handled.
        """
        self.attack_cooldown = self.time_to_execute_pattern+1000
        self.angle_for_attack = Vector2D(-1,0)\
                                if player.position.x > self.position.x\
                                else Vector2D(1,0)
        laser = Laser(self.centre_position(),
                      self.angle_for_attack,
                      self.current_movement_pattern.time_laser_attack())
        edge_laser_behaviour =[Laser.LaserMovement.AcceleratingStart,
                               Laser.LaserMovement.DeceleratingEnd]
        laser.set_type(edge_laser_behaviour, pi/2,  pi, pi/9)
        boss_lasers.add(laser)
        if self.current_movement_pattern == BossAI.MovePattern.StandInMiddle:
            laser2 = Laser(self.centre_position(),
                           self.angle_for_attack,
                           self.current_movement_pattern.time_laser_attack())
            laser2.set_type(
                edge_laser_behaviour,
                pi/2,
                pi,
                pi/9)
            laser2.direction.angle_rotate(pi)
            boss_lasers.add(laser2)

    def _shoot_spiral_bullets(self,
                              boss_bullets: list["Bullet"],
                              player: "Player")  -> None:
        """
        Executes the edge laser attack pattern.
        Adds one laser pointing away from the player.
        Sets the laser to fast speed, sets it to
        accelerate in the beggining and decelerate
        at the end.

        parameters:
        player:
            to set the starting angle away from the player

        set of bullets:
            to add the bullets so they can be handled
        """
        if self.angle_for_attack is None:
            self.angle_for_attack = Vector2D(-1,0)\
                                    if player.position.x > self.position.x\
                                    else Vector2D(1,0)
        boss_bullets.add(
            Bullet(self.centre_position(),
            self.centre_position() + self.angle_for_attack,
            BOSS_ATTACK_COLOR,
            BOSS_BULLET_SIZE))
        if self.current_movement_pattern == BossAI.MovePattern.StandInMiddle:
            boss_bullets.add(
                Bullet(self.centre_position(),
                self.centre_position()\
                + self.angle_for_attack.angle_rotated(pi),
                BOSS_ATTACK_COLOR,
                BOSS_BULLET_SIZE))
        self.angle_for_attack.angle_rotate(BOSS_SPIRAL_SHOOT_ATTACK_ROTATION)
        self.attack_cooldown = BOSS_SPIRAL_ATTACK_COOLDOWN


    def _evaluate_parabolic_movement(self) -> None:
        """
        Evaluates the current movement of the boss depending on
        the time left to execute the movement pattern.

        todo!
        """
        blend = 1 - self.time_to_execute_pattern\
                    / self.current_movement_pattern.get_time()
        if blend<0.1 or blend>0.9:
            self.can_attack = False
        else:
            self.can_attack = True
        #evaluating the x axis positin for the elipse
        #(they are the same for both centres)
        boss_postion_x = blend\
                        * (BOSS_UPPER_CENTRE_OF_ELIPSE.x + BOSS_ELIPSE_WIDTH)
        width_of_elipse_power_2 = BOSS_ELIPSE_WIDTH**2
        elx = ((boss_postion_x - BOSS_UPPER_CENTRE_OF_ELIPSE.x)**2)\
                / width_of_elipse_power_2

        if self.movement_variant == 1:
            #evaluating the y length of the elipse
            #so we can get the position
            length_of_elipse_power_2 = BOSS_ELIPSE_HEIGHT**2
            boss_position_y = sqrt((1 - elx)*length_of_elipse_power_2)\
                              - BOSS_UPPER_CENTRE_OF_ELIPSE.y
            self.position = Vector2D(boss_postion_x, boss_position_y)

        if self.movement_variant == 2:
            #evaluating the y length of the elipse
            #so we can get the position
            length_of_elipse_power_2 = BOSS_ELIPSE_HEIGHT**2
            boss_postion_y = sqrt((1 - elx)*length_of_elipse_power_2)\
                             + BOSS_LOWER_CENTRE_OF_ELIPSE.y

            #getting the mirror image of y,
            #so we can invert the half elipse
            #and moving it to the correct position
            boss_postion_y = -boss_postion_y + 2*BOSS_LOWER_CENTRE_OF_ELIPSE.y
            self.position = Vector2D(boss_postion_x, boss_postion_y)

    def _evaluate_stand_in_middle_movement(self) -> None:
        """
        Evaluates the current movement of the boss depending on
        the time left to execute the movement pattern.

        todo!
        """
        blend = self.time_to_execute_pattern\
                / self.current_movement_pattern.get_time()
        if blend<=0.2 or blend>=0.8:
            self.can_attack = False
            current_blend = blend*5 if blend<=0.2 else (blend - 0.8)*5 + 1
            current_blend /= 2
            if self.movement_variant in [2,4]:
                current_blend = 1 - current_blend # opposite
            if self.movement_variant in [1,2]:
                self.position =\
                    current_blend*Vector2D(0, CENTRE_OF_MAP.y)\
                    + (1 - current_blend)\
                    * Vector2D(CENTRE_OF_MAP.x*2, CENTRE_OF_MAP.y)
            else:
                self.position =\
                    current_blend*Vector2D(CENTRE_OF_MAP.x, 0)\
                    + (1 - current_blend)\
                    * Vector2D(CENTRE_OF_MAP.x, CENTRE_OF_MAP.y*2)
        else:
            self.can_attack = True
            self.position = CENTRE_OF_MAP
