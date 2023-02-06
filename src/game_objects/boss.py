import pygame
from src.classes.game_object import GameObject
from src.classes.vector_2d import number_types
from src.classes.boss_ai import BossAI, MovePatternType, EasyAttackPattern
from src.game_objects.player import Player
from src.game_objects.bullet import Bullet
from src.game_values import *
from src.game_objects.laser import Laser


class Boss(BossAI, GameObject):
    """
    Boss object to battle with player.
    Has AI to handle movement and attack patterns.
    """
    def __init__(self,
        boss_sprite: "pygame.Surface",
        width: number_types = 64,
        height: number_types = 64) -> None:
        """Initialisation of Boss object."""

        BossAI.__init__(self)
        GameObject.__init__(self, Vector2D(0,0))
        self.sprite = pygame.transform.scale(boss_sprite, (width, height))
        self.width = width
        self.height = height
        self.rotation = 0
        self.radius = width/2
        self.active = False
        self.sleep_time = 0
        self.health = BOSS_HEALTH

    def activate(self):
        """
        Boss starts to execute patterns and to attack.
        """
        self.active = True

    def deactivate(self):
        """
        Boss stops to executing patterns and attacking.
        """
        self.active = False

    def _move(self) -> None:
        """
        Moves the boss object with the correspoinding move pattern.
        """
        if self.current_movement_pattern.type\
            == MovePatternType.ParabolicMovement:
            self._evaluate_parabolic_movement()
        if self.current_movement_pattern.type\
            == MovePatternType.StandInMiddle:
            self._evaluate_stand_in_middle_movement()

    def _execute_attack_pattern(self,
            player: "Player",
            boss_bullets: list["Bullet"],
            boss_lasers: list["Laser"]) -> None:
        """
        Calls the right attack pattern depending on if hardmode is on or off.
        """
        if self.hardmode:
            self._execute_hard_attack_pattern(player, boss_bullets, boss_lasers)
        else:
            self._execute_easy_attack_pattern(player, boss_bullets, boss_lasers)
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
        if self.active:
            if self.sleep_time < 0:
                self.time_to_execute_pattern -= clock.get_time()
                self.attack_cooldown -= clock.get_time()
                self._evaluate_attack_pattern()
                self._move()
                if self.attack_cooldown <=0:
                    self._execute_attack_pattern(player, boss_bullets, boss_lasers)
            else:
                self.sleep_time -= clock.get_time()


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

    def take_damage(self, amount):
        self.health -= amount
