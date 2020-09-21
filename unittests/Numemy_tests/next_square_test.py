import unittest
import sys

sys.path.insert(1, '../../src')
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

    def test_next_square_at_exit(self):
        self.numemy.location = (1, 1)
        self.grid.route_dict = {(1, 1): [(1, 1)]}
        self.assertEqual(self.numemy.next_square(self.grid), (1, 1))


if __name__ == '__main__':
    unittest.main()
