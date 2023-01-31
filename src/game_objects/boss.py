import pygame

from src.classes.vector_2d import number_types
from src.classes.boss_ai import BossAI
from src.game_objects.player import Player
from src.game_objects.bullet import Bullet
from src.game_values import *
from src.game_objects.laser import Laser


class Boss(BossAI):
    """
    Boss object to battle with player.
    Has AI to handle movement and attack patterns.
    """
    def __init__(self,
        boss_sprite: "pygame.Surface",
        width: number_types = 64,
        height: number_types = 64) -> None:
        """Initialisation of Boss object."""

        super().__init__()
        self.sprite = pygame.transform.scale(boss_sprite, (width, height))
        self.width = width
        self.height = height
        self.rotation = 0

    def _execute_attack_pattern(self,
    player: "Player",
    boss_bullets: set["Bullet"],
    boss_lasers: set["Laser"]) -> None:
        """
        Calls to the corresponding function to execute the attack pattern.
        Calls only if able to attack at the given moment.

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
                == BossAI.FollowingAttackPattern.WaveShots\
            and self.time_to_execute_pattern\
                > self.current_movement_pattern.cooldown_for_wave_shoot():
            self._shoot_bullet_wave(player, boss_bullets)

        elif self.current_attack_pattern\
            == BossAI.FollowingAttackPattern.PlusLaser:
            self._add_plus_lasers(boss_lasers)


        elif self.current_attack_pattern\
            == BossAI.FollowingAttackPattern.EdgeLaser:
            self._add_edge_laser(player, boss_lasers)

        elif self.current_attack_pattern\
            == BossAI.FollowingAttackPattern.SpiralShoot:
            self._shoot_spiral_bullets(boss_bullets, player)

    def _choose_attack_sequence(self)-> None:
        """
        Creates new attack pattern sequence and adds it to the queue.
        todo!
        """
        #for attack in sample(following_attacks, 3):
        #    self.attack_sequence.put(attack)
        self.attack_sequence.put(BossAI.FollowingAttackPattern.EdgeLaser)
        self.attack_sequence.put(BossAI.FollowingAttackPattern.SpiralShoot)
        self.attack_sequence.put(BossAI.FollowingAttackPattern.PlusLaser)
        self.attack_sequence.put(BossAI.FollowingAttackPattern.WaveShots)

    def _evaluate_attack_pattern(self) -> None:
        """
        Sets new atatck pattern if the old one is finished.
        Takes care of cooldowns
        """
        if self.time_to_execute_pattern <= 0:
            if self.attack_sequence.empty():
                self._choose_attack_sequence()
            self.current_attack_pattern = self.attack_sequence.get()
            self.attack_cooldown = 500
            self.angle_for_attack = None
            self.can_attack = True
            self._pick_new_movement_pattern()
            self.time_to_execute_pattern =\
                self.current_movement_pattern.get_time()

    def _move(self) -> None:
        """
        Moves the boss object with the correspoinding move pattern.
        """
        if self.current_movement_pattern == Boss.MovePattern.ParabolicMovement:
            self._evaluate_parabolic_movement()
        if self.current_movement_pattern == Boss.MovePattern.StandInMiddle:
            self._evaluate_stand_in_middle_movement()


    def main(self,
            player: "Player",
            boss_bullets: list["Bullet"],
            boss_lasers: list["Laser"],
            clock: "pygame.time.Clock") -> None:
        """
        Main call to the player object.
        Evaluates the cooldowns of the boss.
        Handles movement, attacks, changes in movement pattern
        and changes in attack patterns.

        Parameters:
            player -
                To know position of player to execute attacks.
            boss_bullets -
                set of bullets to add new bullets in to be handled.
            boss_lasers -
                set of lasers to add new lasers in to be handled.
            clock -
                to get time from last call to subtract from cooldowns.
        """
        self.time_to_execute_pattern -= clock.get_time()
        self.attack_cooldown -= clock.get_time()
        self._evaluate_attack_pattern()
        self._move()
        if self.attack_cooldown <=0:
            self._execute_attack_pattern(player, boss_bullets, boss_lasers)

    def render(self, display: "pygame.Surface") -> None:
        """
        Handles rendering on screen of the boss object.

        Parameters:
            display -
                Surface to render the boss on.
        """
        rotated_sprite = pygame.transform.rotate(self.sprite, self.rotation)
        position_to_print_on =\
            (self.position.x\
            - (rotated_sprite.get_width() - self.sprite.get_width())/2,
            self.position.y\
            - (rotated_sprite.get_height() - self.sprite.get_height())/2)
        if self.visible:
            display.blit(\
                rotated_sprite,
                position_to_print_on)
