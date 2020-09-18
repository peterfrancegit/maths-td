import unittest
import sys

sys.path.insert(1, '../../src')

from Numemy import Numemy


class TestNextSquare(unittest.TestCase):
    route_dict = {(1, 1): [(1, 1), (1, 2)]}
    def test_next_square(self):
        numemy = Numemy(None, None, None, None, (1, 1), None)
        numemy.next_square()
        self.assertEqual(numemy.location, (1, 2))


if __name__ == '__main__':
    unittest.main()
