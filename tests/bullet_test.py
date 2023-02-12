import unittest
import pygame
from src.classes.vector_2d import Vector2D
from src.game_objects.bullet import Bullet

class FakeClock():
    def __init__(self, time):
        self.time = time

    def get_time(self):
        return self.time

class TestingBullet(unittest.TestCase):

    def test_moving_bullet(self):
        bullet = Bullet(Vector2D(0,0), Vector2D(0,1), None, None, 1)
        fake_clock = FakeClock(1000)

        bullet.move(fake_clock)
        self.assertEqual(bullet.position,  Vector2D(0,1))
        bullet.move(fake_clock)
        self.assertEqual(bullet.position,  Vector2D(0,2))
        bullet.move(fake_clock)
        self.assertEqual(bullet.position,  Vector2D(0,3))

    def test_invalidation(self):
        bullet = Bullet(Vector2D(-1,-1), Vector2D(0,1))
        self.assertEqual(bullet.valid, True)
        bullet.invalidate()
        self.assertNotEqual(bullet.valid, True)

    def test_bullet_out_of_bounds(self):
        bullet = Bullet(Vector2D(-1,-1), Vector2D(0,1))
        bullet.check_boundaries()
        self.assertNotEqual(bullet.valid, True)