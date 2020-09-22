import unittest
from unittest.mock import Mock
from io import StringIO
import sys

sys.path.insert(1, '../src')
import pygame
from Grid import Grid
from Square import Square
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

        screenWidth, screenHeight = (500, 500)
        self.display.get_size.return_value = (screenWidth, screenHeight)
        self.grid.initialise_square_grid(self.display)
        self.grid.initialise_exit()

    
        self.assertTrue(isinstance(self.grid.square_grid[self.grid.exit_square[0]][self.grid.exit_square[1]], Exit))

    def test_initialise_exit_when_square_grid_not_initialised(self):
        """Tests if initialise_exit prints the correct message when the grid instance variable square_grid has not been initialised"""
        
        # Sets the return value for function get_size
        screenWidth, screenHeight = (500, 500)
        self.display.get_size.return_value = (screenWidth, screenHeight)

        stdout = StringIO()
        sys.stdout = stdout

        #self.grid.initialise_square_grid(self.display)
        self.grid.initialise_exit()

        sys.stdout = sys.__stdout__
        self.assertEqual("Instance variable square_grid has not been intialised properly.  Please call the method initialise_square_grid to initialise it.\n", 
        stdout.getvalue())


if __name__ == '__main__':
    unittest.main()
