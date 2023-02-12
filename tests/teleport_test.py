import unittest
import pygame
from src.classes.vector_2d import Vector2D
from src.game_objects.teleport import Teleport

class FakeClock():
    def __init__(self, time):
        self.time = time

    def get_time(self):
        return self.time

class TestingTeleport(unittest.TestCase):

    def test_activate_teleport(self):
        teleport = Teleport(1, pygame.Surface((1,1)), Vector2D(1,1))
        self.assertEqual(teleport.active,  False)

        teleport.activate(Vector2D(0,0), Vector2D(0,1))
        self.assertEqual(teleport.active,  True)


    def test_moving_teleport(self):
        teleport = Teleport(1, pygame.Surface((1,1)), Vector2D(1,1))
        fake_clock = FakeClock(1000)

        teleport.activate(Vector2D(0,0), Vector2D(0,1))

        self.assertEqual(teleport.position,  Vector2D(0,0))
        teleport.move(fake_clock)
        self.assertNotEqual(teleport.position,  Vector2D(0,1))
        teleport.move(fake_clock)
        self.assertNotEqual(teleport.position,  Vector2D(0,2))


    def test_teleport_out_of_bounds(self):
        teleport = Teleport(1, pygame.Surface((1,1)), Vector2D(1,1))

        teleport.activate(Vector2D(0,0), Vector2D(0,1))
        teleport.check_boundaries()
        self.assertEqual(teleport.movement, Vector2D(0,1))
        teleport.deactivate()

        teleport.activate(Vector2D(0,0), Vector2D(0,-1))
        teleport.check_boundaries()
        self.assertEqual(teleport.movement, Vector2D(0,1))