import unittest
import sys

sys.path.insert(1, '../../src')

from Numemy import Numemy


class TestTakeDamage(unittest.TestCase):
    def test_take_damage_add(self):
        numemy = Numemy(None, 10, None, None, None, None)
        numemy.take_damage('+', 10)
        self.assertEqual(numemy.value, 20)

    def test_take_damage_subtract(self):
        numemy = Numemy(None, 10, None, None, None, None)
        numemy.take_damage('-', 10)
        self.assertEqual(numemy.value, 0)

    def test_take_damage_multiply(self):
        numemy = Numemy(None, 10, None, None, None, None)
        numemy.take_damage('*', 2)
        self.assertEqual(numemy.value, 20)

    def test_take_damage_divide(self):
        numemy = Numemy(None, 10, None, None, None, None)
        numemy.take_damage('/', 2)
        self.assertEqual(numemy.value, 5)


if __name__ == '__main__':
    unittest.main()
