import unittest
from unittest.mock import Mock
from io import StringIO
import sys

from dijkstar import Graph
sys.path.insert(1, '../src')
from Grid import Grid, find_route
from Square import Exit


class GridTests(unittest.TestCase):

    def setUp(self):
        """Creates a Grid object for the tests"""
        self.grid = Grid(None, None, None, None, None)
        self.display = Mock()

# initialise_dijk_grid() tests
    def test_initialise_dijk_grid_no_blocks(self):
        self.grid.width, self.grid.height, self.grid.blocks = 2, 2, []
        self.grid.initialise_dijk_grid()
        test_grid = Graph()
        for i in range(2):
            test_grid.add_edge((i, 0), (i, 1), 1)
            test_grid.add_edge((i, 1), (i, 0), 1)
            test_grid.add_edge((0, i), (1, i), 1)
            test_grid.add_edge((1, i), (0, i), 1)
        self.assertEqual(self.grid.dijk_grid, test_grid)

    def test_initialise_dijk_grid_simple(self):
        self.grid.width, self.grid.height, self.grid.blocks = 2, 2, [(1, 1)]
        self.grid.initialise_dijk_grid()
        test_grid = Graph()
        for i in range(2):
            test_grid.add_edge((i, 0), (i, 1), 1)
            test_grid.add_edge((i, 1), (i, 0), 1)
            test_grid.add_edge((0, i), (1, i), 1)
            test_grid.add_edge((1, i), (0, i), 1)
        test_grid.remove_node((1, 1))
        self.assertEqual(self.grid.dijk_grid, test_grid)

    def test_initialise_dijk_grid_all_blocks(self):
        self.grid.width, self.grid.height, self.grid.blocks = 2, 2, [(0, 0), (0, 1), (1, 0), (1, 1)]
        self.grid.initialise_dijk_grid()
        test_grid = Graph()
        self.assertEqual(self.grid.dijk_grid, test_grid)

# find_route() tests
    def test_find_route_no_blocks_max_dist(self):
        self.grid.width, self.grid.height, self.grid.blocks = 10, 10, []
        self.grid.initialise_dijk_grid()
        spawner, exit = (0, 0), (9, 9)
        route = [(row, 0) for row in range(10)] + [(9, col) for col in range(1, 10)]
        self.assertEqual(find_route(self.grid.dijk_grid, spawner, exit), route)

# initialise_exit() tests
    def test_initialise_exit(self):
        """Tests if the initialise_square_grid function initialises the square_grid variable in the given grid object correctly"""

        self.grid.width, self.grid.height, self.grid.exit_square = 10, 10, (4, 9)
        # Sets the return value for the mock objects .get_size() method return

        screenWidth, screenHeight = (500, 500)
        self.display.get_size.return_value = (screenWidth, screenHeight)
        self.grid.initialise_square_grid(self.display)
        self.grid.initialise_exit()

    
        self.assertTrue(isinstance(self.grid.square_grid[self.grid.exit_square[0]][self.grid.exit_square[1]][1], Exit))

    def test_initialise_exit_when_square_grid_not_initialised(self):
        """Tests if initialise_exit prints the correct message when the grid instance variable square_grid has not been initialised"""

        self.grid.exit_square = (4, 9)
        # Sets the return value for function get_size
        screenWidth, screenHeight = (500, 500)
        self.display.get_size.return_value = (screenWidth, screenHeight)

        stdout = StringIO()
        sys.stdout = stdout

        self.grid.initialise_exit()

        sys.stdout = sys.__stdout__
        self.assertEqual("Instance variable square_grid has not been initialised properly. Please call the method initialise_square_grid to initialise it.\n",
        stdout.getvalue())


if __name__ == '__main__':
    unittest.main()
