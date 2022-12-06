from src.classes import Vector2D
import unittest


class TestingVector(unittest.TestCase):

    def test_creating_vectors(self):
        vector1 = Vector2D(1,-1)
        self.assertEqual(vector1.x, 1)
        self.assertEqual(vector1.y, -1)
        self.assertEqual(vector1.x, vector1.x)

        vector2 = Vector2D(1,-2)
        self.assertEqual(vector1.x, vector2.x)
        self.assertNotEqual(vector1.y, vector2.y)
        self.assertEqual(vector1.y, vector1.y)

if __name__ == '__main__':
    unittest.main()