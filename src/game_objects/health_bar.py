import pygame, sys
from src.classes.game_object import GameObject
from src.classes.vector_2d import Vector2D
from src.game_values import *
class HealthBar(pygame.sprite.Sprite, GameObject):
    """
    HealthBar for the boss
    """
    def __init__(self, position: "Vector2D"):
        pygame.sprite.Sprite.__init__(self)
        GameObject.__init__(self, position)
        self.image = pygame.Surface(tuple(position))
        self.image.fill((200,30,30))
        self.rect = self.image.get_rect(center = (400,400))
        self.current_health = BOSS_HEALTH
        self.target_health = BOSS_HEALTH
        self.max_health = BOSS_HEALTH
        self.health_bar_length = 800
        self.health_ratio = self.max_health / self.health_bar_length
        self.health_change_speed = 1

    def set_health(self, amount):
        self.target_health = amount

    def main(self):
        pass


    def render(self, screen: "pygame.Surface"):
        transition_width = 0
        transition_color = (255,0,0)

        if self.current_health > self.target_health:
            self.current_health -= self.health_change_speed
            transition_width = int((self.target_health - self.current_health) / self.health_ratio)
            transition_color = (255,255,0)

        health_bar_width = int(self.current_health / self.health_ratio)
        health_bar = pygame.Rect(self.position.x,self.position.y,health_bar_width,25)
        transition_bar = pygame.Rect(health_bar.right,self.position.y,transition_width,25)

        pygame.draw.rect(screen,(255,0,0),health_bar)
        pygame.draw.rect(screen,transition_color,transition_bar)
        pygame.draw.rect(screen,(255,255,255),(self.position.x,self.position.y,self.health_bar_length,25),4)