from src.game_objects.player import Player
from src.classes.vector_2d import Vector2D
from src.game_objects.bullet import Bullet
import unittest


class FakeClock():
    def __init__(self, time):
        self.time = time

    def get_time(self):
        return self.time

class TestingVector(unittest.TestCase):

    def test_moving_player(self):
        player = Player(Vector2D(0,0), 1, None)
        fake_clock = FakeClock()

        player.move([False,False,False,False], fake_clock)
        self.assertEqual(player.position,  Vector2D(0,0))
        self.assertNotEqual(player.rotation, 0)

        player.move([False,False,False,True], fake_clock)
        self.assertEqual(player.position, Vector2D(0,1))

        player.move([False,False,True,False], fake_clock)
        self.assertEqual(player.position, Vector2D(0,0))

        player.move([False,True,False,False], fake_clock)
        self.assertEqual(player.position, Vector2D(1,0))

        player.move([True,False,False,False], fake_clock)
        self.assertEqual(player.position, Vector2D(0,0))

        player.move([False,False,True,True], fake_clock)
        self.assertEqual(player.position, Vector2D(0,0))

        player.move([True,True,False,False], fake_clock)
        self.assertEqual(player.position, Vector2D(0,0))

        player.move([True,False,False,True], fake_clock)
        self.assertEqual(player.position, Vector2D(-1,1))

        player.move([True,True,True,True], fake_clock)
        self.assertEqual(player.position, Vector2D(-1,1))

    def test_player_firing(self):
        player = Player(Vector2D(0,0), 1, None)
        bullet_set = set()
        player.fire(bullet_set, Vector2D(1,1))

        self.assertEqual(player.fire_cooldown > 0)
        for bullet in bullet_set:
            self.assertEqual(isinstance(bullet, Bullet), True)

