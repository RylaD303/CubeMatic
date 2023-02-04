from random import randint, sample, choice
from queue import Queue
from enum import Enum
from math import pi, sqrt
from typing import Union
from src.classes.vector_2d import Vector2D, number_types
from src.game_objects.player import Player
from src.game_objects.bullet import Bullet
from src.game_values import *
from src.game_objects.laser import Laser, LaserMovement


class EasyAttackPattern(Enum):
    """
    Easy Attack patterns for boss.
    """
    WaveShots = 1
    PlusLaser = 2
    EdgeLaser = 3
    SpiralShoot = 4
    CircleShoot = 5

class HardAttackPattern(Enum):
    """
    Hard Attack patterns for boss.
    """
    CircleShotsWithEdgeLaser = 1
    CircleShotsWithPlusLaser = 2
    DoublePlusLaser = 3
    DoubleEdgeLaser = 4
    SpiralShotsWithPlusLaser = 5
    SpiralShotsWithEdgeLaser = 6

class MovePatternType(Enum):
    """
    Enum for state of movement pattern of the boss.
    """
    StandInMiddle = 1
    ParabolicMovement = 2


class MovePattern():
    """
    Class to evaluate move_patterns
    """
    evaluations = {
    MovePatternType.StandInMiddle: {
                        "time_to_execute": 10000,
                        "time_for_one_laser_attack":7500,
                        "cooldown_for_wave_shoot":
                        BOSS_WAVE_SHOOT_COOLDOWN},
    MovePatternType.ParabolicMovement: {
                            "time_to_execute": 8000,
                            "time_for_one_laser_attack":6800,
                            "cooldown_for_wave_shoot":
                            BOSS_WAVE_SHOOT_COOLDOWN}}

    def __init__(self, move_pattern_type: "MovePatternType"):
        """
        Creates MovePattern for the boss to evaluate
        move pattern types.
        """
        self.type = move_pattern_type

    def get_time(self) -> number_types:
        """
        Returns the enums corresponding time to
        execute movement patter
        """
        return self.evaluations[self.type]["time_to_execute"]
    def time_laser_attack(self)  -> number_types:
        """
        Returns the enums corresponding time to
        execute laser attack pattern
        """
        return self.evaluations[self.type]["time_for_one_laser_attack"]
    def cooldown_for_wave_shoot(self)  -> number_types:
        """
        Returns the enums corresponding cooldown for
        wave shoot attack pattern
        """
        return self.evaluations[self.type]["cooldown_for_wave_shoot"]

class BossAI():
    """
    BossAI object.
    Handles the movement patterns and the attack patterns of
    the Boss. Value of enums is ID.
    """

    easy_attacks = list(EasyAttackPattern)
    hard_attacks = list(HardAttackPattern)
    movement_pattern_types = list(MovePatternType)

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

        #self.speed = speed
        #self.width = width
        #self.height = height
        self.current_movement_pattern: MovePattern = None
        self.movement_variant: int = 0
        self.attack_sequence: "Queue" = Queue()
        self.current_attack_pattern:\
            Union["EasyAttackPattern", "HardAttackPattern"] = None
        self.attack_cooldown: float = 0
        self.hard_attack_executed: bool = False
        self.angle_for_attack: float = None
        self.can_attack: bool = False
        self.time_to_execute_pattern: float = 0
        self.hardmode: bool = False

    def centre_position(self) -> "Vector2D":
        """
        Returns the centre position of the Boss,
        depending on its scale.

        return_t: Vector2D
        """
        return self.position + BOSS_SCALE/2

    def _start_hardmode(self):
        """
        Starts the hard attack of the boss.
        Clears the easy attack in the queue, so the next attacks
        in the sequence can be hard.
        """
        #self.attack_sequence.clear()
        self.attack_sequence = Queue()
        #didn't find how to empty a queue on the internet LOL
        self.hardmode = True

    def _pick_new_movement_pattern(self)  -> None:
        """
        Sets new movement pattern and movement variant for the boss.
        """
        new_movement_pattern = choice(BossAI.movement_pattern_types)
        self.current_movement_pattern =\
            MovePattern(new_movement_pattern)
        if new_movement_pattern == MovePatternType.ParabolicMovement:
            self.movement_variant = randint(1,2)
        if new_movement_pattern == MovePatternType.StandInMiddle:
            self.movement_variant = randint(1,4)


    def _shoot_bullet_wave(self, player: "Player",
                           boss_bullets: set["Bullet"])  -> None:
        """
        Executes attack waveshoot:
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
        bullet0 =Bullet(self.centre_position(),
                        player.position,
                        BOSS_ATTACK_COLOR,
                        BOSS_BULLET_SIZE,
                        BOSS_WAVE_SHOOT_BULLET_STARTING_SPEED)
        bullet0.set_slowdown_speed(-BOSS_WAVE_SHOOT_BULLET_INCREASING_SPEED)
        boss_bullets.add(bullet0)
        #side nnullets
        for i in range(1,3):
            bullet1 = Bullet(
                self.centre_position(),
                player.position,
                BOSS_ATTACK_COLOR,
                BOSS_BULLET_SIZE,
                BOSS_WAVE_SHOOT_BULLET_STARTING_SPEED)
            bullet1.set_slowdown_speed(-BOSS_WAVE_SHOOT_BULLET_INCREASING_SPEED)
            bullet1.movement.angle_rotate(i*BOSS_WAVE_SHOOT_ANGLE)
            boss_bullets.add(bullet1)
            bullet2 = Bullet(
                self.centre_position(),
                player.position,
                BOSS_ATTACK_COLOR,
                BOSS_BULLET_SIZE,
                BOSS_WAVE_SHOOT_BULLET_STARTING_SPEED)
            bullet2.set_slowdown_speed(-BOSS_WAVE_SHOOT_BULLET_INCREASING_SPEED)
            bullet2.movement.angle_rotate(-i*BOSS_WAVE_SHOOT_ANGLE)
            boss_bullets.add(bullet2)

    def _add_plus_laser(self, boss_lasers: set["Laser"])  -> None:
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
        plus_laser_behaviour = [LaserMovement.AcceleratingStart,
                                LaserMovement.DeceleratingEnd]
        for laser in lasers:
            laser.set_type(plus_laser_behaviour,
                            BOSS_PLUS_LASER_ROTATION_SPEED,
                            BOSS_PLUS_LASER_MAXIMUM_SPEED,
                            BOSS_PLUS_LASER_MINIMUM_SPEED)
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
        self.attack_cooldown = self.time_to_execute_pattern+SECOND
        self.angle_for_attack = Vector2D(-1,0)\
                                if player.position.x > self.position.x\
                                else Vector2D(1,0)
        laser = Laser(self.centre_position(),
                      self.angle_for_attack,
                      self.current_movement_pattern.time_laser_attack())
        edge_laser_behaviour =[LaserMovement.AcceleratingStart,
                               LaserMovement.DeceleratingEnd]
        laser.set_type(edge_laser_behaviour,
                        BOSS_EDGE_LASER_ROTATION_SPEED,
                        BOSS_EDGE_LASER_MAXIMUM_SPEED,
                        BOSS_EDGE_LASER_MINIMUM_SPEED)

        boss_lasers.add(laser)
        if self.current_movement_pattern.type == MovePatternType.StandInMiddle\
            and not self.hardmode:
            laser2 = Laser(self.centre_position(),
                           self.angle_for_attack,
                           self.current_movement_pattern.time_laser_attack())
            laser2.set_type(
                edge_laser_behaviour,
                BOSS_EDGE_LASER_ROTATION_SPEED,
                BOSS_EDGE_LASER_MAXIMUM_SPEED,
                BOSS_EDGE_LASER_MINIMUM_SPEED)
            laser2.direction.angle_rotate(pi)
            boss_lasers.add(laser2)

    def _shoot_spiral_bullets(self,
                              player: "Player",
                              boss_bullets: list["Bullet"])  -> None:
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
            BOSS_BULLET_SIZE,
            BOSS_SPIRAL_SHOOT_BULLET_SPEED))
        if self.current_movement_pattern.type == MovePatternType.StandInMiddle:
            boss_bullets.add(
                Bullet(self.centre_position(),
                self.centre_position()\
                + self.angle_for_attack.angle_rotated(pi),
                BOSS_ATTACK_COLOR,
                BOSS_BULLET_SIZE,
                BOSS_SPIRAL_SHOOT_BULLET_SPEED))
        self.angle_for_attack.angle_rotate(BOSS_SPIRAL_SHOOT_ROTATION)
        self.attack_cooldown = BOSS_SPIRAL_COOLDOWN

    def _shoot_circle_bullets(self, boss_bullets: set["Bullet"]):
        """
        Executes the shoot circle attack patter.

        set of bullets:
            to add the bullets so they can be handled
        """
        if self.angle_for_attack is None:
            self.angle_for_attack = Vector2D(-1,0)
        number_of_bullets  = round(pi/BOSS_CIRCLE_SHOOT_ROTATION)
        for index in range(number_of_bullets*2):
            boss_bullets.add(
                Bullet(self.centre_position(),
                self.centre_position()\
                + self.angle_for_attack.angle_rotated(index*BOSS_CIRCLE_SHOOT_ROTATION),
                BOSS_ATTACK_COLOR,
                BOSS_BULLET_SIZE,
                BOSS_CIRCLE_SHOOT_BULLET_SPEED))
        self.attack_cooldown = BOSS_CIRCLE_SHOOT_COOLDOWN
        self.angle_for_attack.angle_rotate(pi/0.2)

    def _evaluate_parabolic_movement(self) -> None:
        """
        Evaluates the current movement of the boss depending on
        the time left to execute the movement pattern.

        todo! documentation
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

        todo! documentation
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

    def _execute_easy_attack_pattern(self,
        player: "Player",
        boss_bullets: set["Bullet"],
        boss_lasers: set["Laser"]) -> None:
        """
        Calls to the corresponding function to execute the easy
        attack pattern. Executes only if able to attack at the given
        moment.

        Paramateres:
            player -
                to know players position
            boss_bullets -
                set of bullets to stack in for handling later.
            boss_lasers -
                set of lasers to stack in for handling later.
        """
        if not self.can_attack:
            return
        if self.current_attack_pattern\
                == EasyAttackPattern.WaveShots\
            and self.time_to_execute_pattern\
                > self.current_movement_pattern.cooldown_for_wave_shoot():
            self._shoot_bullet_wave(player, boss_bullets)

        elif self.current_attack_pattern\
            == EasyAttackPattern.PlusLaser:
            self._add_plus_laser(boss_lasers)


        elif self.current_attack_pattern\
            == EasyAttackPattern.EdgeLaser:
            self._add_edge_laser(player, boss_lasers)

        elif self.current_attack_pattern\
            == EasyAttackPattern.SpiralShoot:
            self._shoot_spiral_bullets(player, boss_bullets)

        elif self.current_attack_pattern\
            == EasyAttackPattern.CircleShoot:
            self._shoot_circle_bullets(boss_bullets)

    def _execute_hard_attack_pattern(self,
        player: "Player",
        boss_bullets: set["Bullet"],
        boss_lasers: set["Laser"]) -> None:
        """
        Calls to the corresponding function to execute the hard
        attack pattern. Executes only if able to attack at the given
        moment.

        Paramateres:
            player -
                to know players position
            boss_bullets -
                set of bullets to stack in for handling later.
            boss_lasers -
                set of lasers to stack in for handling later.
        """
        if not self.can_attack:
            return

        if self.current_attack_pattern\
            == HardAttackPattern.CircleShotsWithEdgeLaser:
            if not self.hard_attack_executed:
                self._add_edge_laser(player, boss_lasers)
                self.hard_attack_executed = True
            self._shoot_circle_bullets(boss_bullets)


        elif self.current_attack_pattern\
            == HardAttackPattern.CircleShotsWithPlusLaser:
            if not self.hard_attack_executed:
                self._add_plus_laser(boss_lasers)
                self.hard_attack_executed = True
            self._shoot_circle_bullets(boss_bullets)

        elif self.current_attack_pattern\
            == HardAttackPattern.DoublePlusLaser:
            if not self.hard_attack_executed:
                self._add_plus_laser(boss_lasers)
                self.hard_attack_executed = True
                self.attack_cooldown = 500
            else:
                self._add_plus_laser(boss_lasers)

        elif self.current_attack_pattern\
            == HardAttackPattern.DoubleEdgeLaser:
            if not self.hard_attack_executed:
                self._add_edge_laser(player, boss_lasers)
                self.hard_attack_executed = True
                self.attack_cooldown = 400
            else:
                self._add_edge_laser(player, boss_lasers)

        elif self.current_attack_pattern\
            == HardAttackPattern.SpiralShotsWithPlusLaser:
            if not self.hard_attack_executed:
                self._add_plus_laser(boss_lasers)
                self.hard_attack_executed = True
            self._shoot_spiral_bullets(player, boss_bullets)

        elif self.current_attack_pattern\
            == HardAttackPattern.SpiralShotsWithEdgeLaser:
            if not self.hard_attack_executed:
                self._add_edge_laser(player, boss_lasers)
                self.hard_attack_executed = True
            self._shoot_spiral_bullets(player, boss_bullets)

    def _choose_attack_sequence(self)-> None:
        """
        Creates new attack pattern sequence and adds it to the queue.
        todo!
        """
        if not self.hardmode:
            for attack in sample(BossAI.easy_attacks, 3):
                self.attack_sequence.put(attack)
        if self.hardmode:
            for attack in sample(BossAI.hard_attacks, 3):
                self.attack_sequence.put(attack)

    def _evaluate_attack_pattern(self) -> None:
        """
        Sets new atatck pattern if the old one is finished.
        Takes care of cooldowns.
        """
        if self.time_to_execute_pattern <= 0:
            if  not self.hardmode\
                 and self.health <= BOSS_HARDMODE_HEALTH_THRESHOLD:
                self._start_hardmode()
            if self.attack_sequence.empty():
                self._choose_attack_sequence()
            self.current_attack_pattern = self.attack_sequence.get()
            self.attack_cooldown = 0
            self.hard_attack_executed = False
            self.angle_for_attack = None
            self.can_attack = True
            self._pick_new_movement_pattern()
            self.time_to_execute_pattern =\
                self.current_movement_pattern.get_time()
            self.sleep_time = 1500

