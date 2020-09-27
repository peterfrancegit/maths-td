import unittest
from unittest.mock import Mock
from io import StringIO
import sys

sys.path.insert(1, '../src')
from Grid import Grid, find_route
from Square import Exit, Spawner, Block
from dijkstar import Graph, NoPathError


class GridTests(unittest.TestCase):

    def setUp(self):
        """Creates a Grid object for the tests"""
        self.grid = Grid(None, None, None, None, None, None)
        self.display = Mock()
        screenWidth, screenHeight = (500, 500)
        # Sets the return value for function get_size
        self.display.get_size.return_value = (screenWidth, screenHeight)

# initialise_dijk_grid() tests
    def test_initialise_dijk_grid_with_no_blocks(self):
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

    def test_initialise_dijk_grid_with_all_blocks(self):
        self.grid.width, self.grid.height, self.grid.blocks = 2, 2, [(0, 0), (0, 1), (1, 0), (1, 1)]
        self.grid.initialise_dijk_grid()
        test_grid = Graph()
        self.assertEqual(self.grid.dijk_grid, test_grid)

# find_route() tests
    def test_find_route_with_no_blocks_and_max_dist(self):
        self.grid.width, self.grid.height, self.grid.blocks = 10, 10, []
        self.grid.initialise_dijk_grid()
        spawner, exit = (0, 0), (9, 9)
        route = [(row, 0) for row in range(10)] + [(9, col) for col in range(1, 10)]
        self.assertEqual(find_route(self.grid.dijk_grid, spawner, exit), route)

    def test_find_route_with_isolated_spawner(self):
        self.grid.width, self.grid.height, self.grid.blocks = 10, 10, [(0, 1), (1, 0)]
        self.grid.initialise_dijk_grid()
        spawner, exit = (0, 0), (9, 9)
        self.assertRaises(NoPathError, find_route, self.grid.dijk_grid, spawner, exit)

# initialise_exit() tests
    def test_initialise_exit_classic(self):
        """Tests if the initialise_exit() function initialises the Exit in the given grid object correctly"""

        self.grid.width, self.grid.height, self.grid.exit_square = 10, 10, (4, 9)

        self.grid.initialise_square_grid(self.display)
        self.grid.initialise_exit(None)

    
        self.assertTrue(isinstance(self.grid.square_grid[self.grid.exit_square[0]][self.grid.exit_square[1]][1], Exit))

    def test_initialise_exit_when_square_grid_not_initialised(self):
        """Tests if initialise_exit prints the correct message when the grid instance variable square_grid has not been initialised"""

        self.grid.exit_square = (4, 9)

        stdout = StringIO()
        sys.stdout = stdout

        self.grid.initialise_exit(None)

        sys.stdout = sys.__stdout__
        self.assertEqual("Instance variable square_grid has not been initialised properly. Please call the method initialise_square_grid to initialise it.\n",
        stdout.getvalue())

# initialise_spawner() tests
    def test_initialise_spawner_classic(self):
        """Tests if the initialise_spawner() function initialises the Spawner in the given grid object correctly"""

        self.grid.width, self.grid.height, self.grid.spawner_square = 10, 10, (5, 6)

        self.grid.initialise_square_grid(self.display)
        self.grid.initialise_spawner()

        self.assertTrue(isinstance(self.grid.square_grid[self.grid.spawner_square[0]][self.grid.spawner_square[1]][1], Spawner))

    def test_initialise_spawner_when_square_grid_not_initialised(self):
        """Tests if initialise_spawner() prints the correct message when the grid instance variable square_grid has not been initialised"""

        self.grid.spawner_square = (6, 7)

        stdout = StringIO()
        sys.stdout = stdout

        self.grid.initialise_spawner()

        sys.stdout = sys.__stdout__
        self.assertEqual("Instance variable square_grid has not been initialised properly. Please call the method initialise_square_grid to initialise it.\n",
        stdout.getvalue())

# initialise_blocks() tests
    def test_initialise_blocks_with_no_blocks(self):
        self.grid.width, self.grid.height, self.grid.blocks = 10, 10, []

        self.grid.initialise_square_grid(self.display)
        self.grid.initialise_blocks()
        for row in range(10):
            for col in range(10):
                self.assertEqual(len(self.grid.square_grid[row][col]), 1)
                self.assertFalse(isinstance(self.grid.square_grid[row][col][0], Block))

    def test_intialise_blocks_with_all_blocks(self):
        self.grid.width, self.grid.height, self.grid.blocks = 10, 10, [(row,col) for row in range(10) for col in range(10)]

        self.grid.initialise_square_grid(self.display)
        self.grid.initialise_blocks()
        for row in range(10):
            for col in range(10):
                    self.assertEqual(len(self.grid.square_grid[row][col]), 2)
                    self.assertFalse(isinstance(self.grid.square_grid[row][col][0], Block))
                    self.assertTrue(isinstance(self.grid.square_grid[row][col][1], Block))

    def test_intialise_blocks_classic(self):
        self.grid.width, self.grid.height, self.grid.blocks = 10, 10, [(2, 3), (4, 7), (5, 6), (9, 8), (2, 4), (3, 1)]

        self.grid.initialise_square_grid(self.display)
        self.grid.initialise_blocks()
        for row in range(10):
            for col in range(10):
                    self.assertFalse(isinstance(self.grid.square_grid[row][col][0], Block))
                    if (row, col) in self.grid.blocks:
                        self.assertEqual(len(self.grid.square_grid[row][col]), 2)
                        self.assertTrue(isinstance(self.grid.square_grid[row][col][1], Block))
                    else:
                        self.assertEqual(len(self.grid.square_grid[row][col]), 1)

    def test_initialise_blocks_when_square_grid_not_initialised(self):
        self.grid.blocks = [(6, 7), (7, 4), (1, 2)]

        stdout = StringIO()
        sys.stdout = stdout

        self.grid.initialise_blocks()

        sys.stdout = sys.__stdout__
        self.assertEqual("Instance variable square_grid has not been initialised properly. Please call the method initialise_square_grid to initialise it.\n",
        stdout.getvalue())


if __name__ == '__main__':
    unittest.main()
