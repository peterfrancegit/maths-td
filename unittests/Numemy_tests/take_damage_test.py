import unittest
import sys

sys.path.insert(1, '../../src')
from Numemy import Numemy


class TestTakeDamage(unittest.TestCase):
    def setUp(self):
        self.numemy = Numemy(None, None, None, None, None)

    def test_take_damage_add(self):
        self.numemy.value = 10
        self.numemy.take_damage('+', 10)
        self.assertEqual(self.numemy.value, 20)

    def test_take_damage_subtract(self):
        self.numemy.value = 10
        self.numemy.take_damage('-', 10)
        self.assertEqual(self.numemy.value, 0)

    def test_take_damage_multiply(self):
        self.numemy.value = 10
        self.numemy.take_damage('*', 2)
        self.assertEqual(self.numemy.value, 20)

    def test_take_damage_divide(self):
        self.numemy.value = 10
        self.numemy.take_damage('/', 2)
        self.assertEqual(self.numemy.value, 5)


if __name__ == '__main__':
    unittest.main()
