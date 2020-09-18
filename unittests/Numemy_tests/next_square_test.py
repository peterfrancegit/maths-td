import unittest
import sys

sys.path.insert(1, '../../src')

from Numemy import Numemy


class TestNextSquare(unittest.TestCase):
    def test_next_square_simple(self):
        route_dict = {(1, 1): [(1, 1), (1, 2)]}
        numemy = Numemy(None, None, None, None, (1, 1), None)
        numemy.next_square()
        self.assertEqual(numemy.location, (1, 2))


if __name__ == '__main__':
    unittest.main()
