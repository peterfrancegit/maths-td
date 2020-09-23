import unittest
import sys

sys.path.insert(1, '../src')
from Grid import Grid
from Numemy import Numemy


class TestNextSquare(unittest.TestCase):
    def setUp(self):
        self.grid = Grid(None, None, None, None, None)
        self.numemy = Numemy(None, None, None, None, None)

    def test_next_square_simple(self):
        self.numemy.location = (1, 1)
        self.grid.route_dict = {(1, 1): [(1, 1), (1, 2), (1, 3)]}
        self.assertEqual(self.numemy.next_square(self.grid), (1, 2))

    def test_next_square_when_already_at_exit(self):
        self.numemy.location = (1, 1)
        self.grid.route_dict = {(1, 1): [(1, 1)]}
        self.assertEqual(self.numemy.next_square(self.grid), (1, 1))

    def test_next_square_on_route_from_block(self):
        self.numemy.location = (1, 1)
        self.grid.route_dict = {(1, 2): [(1, 2), (1, 3)]}
        self.assertRaises(KeyError, self.numemy.next_square, self.grid)

    def test_escape_simple(self):
        self.grid.lives = 20
        self.numemy.weight = 5
        self.grid.initialise_square_grid()
        self.numemy.escape(self.grid)
        self.assertEqual(self.grid.lives, 15)

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

    def test_take_damage_divide_by_zero(self):
        self.numemy.value = 10
        self.assertRaises(ZeroDivisionError, self.numemy.take_damage, '/', 0)


if __name__ == '__main__':
    unittest.main()
