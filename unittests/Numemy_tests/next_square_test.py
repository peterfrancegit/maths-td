import unittest
import sys

sys.path.insert(1, '../../src')

from Numemy import Numemy


class TestNextSquare(unittest.TestCase):
    def test_next_square_simple(self):
        route_dict = {(1, 1): [(1, 1), (1, 2), (1, 3)]}
        numemy = Numemy(None, None, None, None, (1, 1), None)
        self.assertEqual(numemy.next_square(route_dict), (1, 2))

    def test_next_square_at_exit(self):
        route_dict = {(1, 1): [(1, 1)]}
        numemy = Numemy(None, None, None, None, (1, 1), None)
        self.assertEqual(numemy.next_square(route_dict), (1, 1))


if __name__ == '__main__':
    unittest.main()
