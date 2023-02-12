import unittest
import pygame
from src.classes.vector_2d import Vector2D
from src.game_objects.laser import Laser, LaserState

class FakeClock():
    def __init__(self, time):
        self.time = time

    def get_time(self):
        return self.time

class TestingLaser(unittest.TestCase):

    def test_state_laser(self):
        laser = Laser(Vector2D(0,0), Vector2D(0,1), 5000)
        fake_clock = FakeClock(550)

        self.assertEqual(laser.state,  LaserState.Anticipation)
        laser.main(fake_clock)
        self.assertEqual(laser.state,  LaserState.Anticipation)
        laser.main(fake_clock)
        self.assertEqual(laser.state,  LaserState.Attack)
        laser.main(fake_clock)
        self.assertEqual(laser.state,  LaserState.Attack)

        laser.switch_state(LaserState.Recovery)
        self.assertEqual(laser.state,  LaserState.Recovery)

    def test_ratoating(self):
        laser = Laser(Vector2D(0,0), Vector2D(0,1), 5000)
        fake_clock = FakeClock(50)

        self.assertEqual(laser.state,  LaserState.Anticipation)
        laser.main(fake_clock)
        self.assertEqual(laser.state,  LaserState.Anticipation)
        self.assertEqual(laser.direction.x, 0)

        laser.switch_state(LaserState.Attack)
        self.assertEqual(laser.state,  LaserState.Attack)

        laser.main(fake_clock)
        self.assertEqual(laser.state,  LaserState.Attack)
        self.assertNotEqual(laser.direction,  Vector2D(0, 1))


    def test_laser_invalidation(self):
        laser = Laser(Vector2D(0,0), Vector2D(0,1), 5000)
        fake_clock = FakeClock(50000)
        laser.switch_state(LaserState.Recovery)
        laser.main(fake_clock)
        self.assertNotEqual(laser.valid, True)