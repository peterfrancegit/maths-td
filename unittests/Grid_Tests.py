import unittest
from unittest.mock import Mock
import sys

sys.path.insert(1, '../src')
import pygame
from Grid import Grid
from Square import Exit

class GridTests(unittest.TestCase):

    def setUp(self):
        """Creates a Grid object for the tests"""

        width = 10
        height = 10
        blocks = []
        spawner_square = (4, 0)
        exit_square = (4, 9)
        self.grid = Grid(width, height, blocks, spawner_square, exit_square)
        self.display = Mock()


    def test_initialise_exit(self):
        """Tests if the initialise_square_grid function initialises the square_grid variable in the given grid object correctly"""
        
        # Sets the return value for the mock objects .get_size() method return
        self.display.get_size.return_value = (500, 500)
        
        self.grid.initialise_square_grid(self.display)
        self.grid.initialise_exit()

    
        self.assertTrue(isinstance(self.grid.square_grid[self.grid.exit_square[0]][self.grid.exit_square[1]], Exit))

    



if __name__ == '__main__':
    unittest.main()
