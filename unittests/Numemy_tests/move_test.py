import unittest
import sys

sys.path.insert(1, '../../src')
from Grid import Grid
from Numemy import Numemy


class TestMove(unittest.TestCase):
    def setUp(self):
        self.grid = Grid(None, None, None, None, None)
        self.numemy = Numemy(None, None, None, None, None)


if __name__ == '__main__':
    unittest.main()
