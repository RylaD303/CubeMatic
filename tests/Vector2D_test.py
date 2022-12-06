from src.classes import Vector2D
import unittest


class TestingVector(unittest.TestCase):

    def test_vectors(self):
        vector1 = Vector2D(1,-1)
        self.assertEqual(sum([2, 3, 5]), 10, "It should be 10")
    def test_sum_tuple(self):
        self.assertEqual(sum((1, 3, 5)), 10, "It should be 10")

if __name__ == '__main__':
    unittest.main()