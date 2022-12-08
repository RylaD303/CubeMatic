from src.classes.Vector2D import Vector2D
import unittest


class TestingVector(unittest.TestCase):

    def test_creating_vectors(self):
        vector1 = Vector2D(1,-1)
        self.assertEqual(vector1.x, Vector2D(1, -1).x)
        self.assertEqual(vector1.x, 1)
        self.assertEqual(vector1.y, -1)
        self.assertEqual(vector1.x, vector1.x)

        vector2 = Vector2D(1,-2)
        self.assertEqual(vector1.x, vector2.x)
        self.assertEqual(vector1.y, vector1.y)

        self.assertNotEqual(vector1.y, vector2.y)

    def test_comparing_vectors(self):
        vector1 = Vector2D(1,-1)
        vector2 = Vector2D(1, -1)
        self.assertEqual(vector1, Vector2D(1, -1))
        self.assertEqual(vector1, (1, -1))
        self.assertEqual(vector1, vector1)
        self.assertEqual(vector1, vector2)

        vector3 = Vector2D(1,-2)
        self.assertNotEqual(vector1, vector3)
        self.assertNotEqual(vector2, vector3)
        self.assertNotEqual(vector3, (-2, 1))

        vector3.y +=1
        self.assertEqual(vector1, vector3)
        self.assertEqual(vector2, vector3)


    def test_adding_vectors(self):
        vector1 = Vector2D(1,-1)
        vector2 = Vector2D(1, -1)
        self.assertEqual(vector1 + vector2, vector1 + vector2)
        self.assertEqual(vector2 + vector2, vector1 + vector2)
        self.assertEqual(vector1 + vector1, vector1 + vector1)
        self.assertEqual(vector1 + vector2, Vector2D(2, -2))

        vector3 = Vector2D(2,-2)
        self.assertEqual(vector3, vector1 + vector2)

        self.assertNotEqual(vector3 + vector1, vector3)
        self.assertEqual(vector3 + vector1, vector1 + Vector2D(1, -1) + vector1)
        self.assertEqual(vector3 - vector1 + vector1, vector3)

    def test_multiplicating_vectors(self):
        vector1 = Vector2D(3,-4)
        vector2 = Vector2D(1, -1)
        self.assertEqual(vector1*vector2, 7)
        self.assertEqual(vector2*vector2, 2)
        self.assertEqual(vector1*Vector2D(2, 2), -2)
        self.assertEqual(vector2*Vector2D(2, -2), 4)

        self.assertEqual(vector1*2, (6, -8))
        self.assertEqual(vector1*-2, (-6, 8))
        self.assertEqual(vector2*vector2*vector2, (2, -2))