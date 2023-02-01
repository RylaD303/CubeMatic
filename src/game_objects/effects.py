import pygame

from src.classes.game_object import GameObject
from src.classes.vector_2d import Vector2D
from src.game_values import *
WHITE=(255,255,255)
class CircleEffect(GameObject):
    """
    Basic circle effect animation.
    Creates illusion of explosion.
    """
    def __init__(self, position: "Vector2D", radius: int) -> None:
       super().__init__(position)
       self.radius = radius
       self.current_radius = radius
       self.time_left = LIFETIME_OF_CIRCLE_EFFECT

    def render(self, display: "pygame.Surface") -> None:
        """Displays aniamtion on screen"""
        pygame.draw.circle( display,
                            WHITE,
                            tuple(self.position),
                            self.current_radius)

    def main(self, clock: "pygame.time.Clock") -> None:
       """Handles the animation expansion, shrinking and validation"""
       self.time_left-=clock.get_time()
       self.current_radius = self.radius*self.time_left/LIFETIME_OF_CIRCLE_EFFECT
       if self.time_left <= 0:
         self.invalidate()

