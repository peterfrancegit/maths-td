from dijkstar import Graph, find_path
from Square import Square, Exit, Spawner
from Numemy import Numemy
from Tower import Tower
import pygame


def find_route(dijk_grid, square, exit_square):
    """Returns list of nodes visited in shortest route from square
    to the exit point"""
    return find_path(dijk_grid, square, exit_square)[0]


class Grid:
    def __init__(self, height, width, blocks, spawner_square, exit_square):
        self.route_dict = {}
        self.height = height
        self.width = width
        self.blocks = blocks
        self.spawner_square = spawner_square
        self.exit_square = exit_square
        self.dijk_grid = Graph()
        self.numemy_list = []
        self.square_grid = []

    def initialise_dijk_grid(self):
        """Initialises the dijk_grid attribute for routing"""
        for i in range(self.height):
            for j in range(self.width):
                if i < self.height - 1:
                    self.dijk_grid.add_edge((i, j), (i + 1, j), 1)
                    self.dijk_grid.add_edge((i + 1, j), (i, j), 1)
                if j < self.width - 1:
                    self.dijk_grid.add_edge((i, j), (i, j + 1), 1)
                    self.dijk_grid.add_edge((i, j + 1), (i, j), 1)
        for node in self.blocks:
            self.dijk_grid.remove_node(node)

    def initialise_route_dict(self):
        """Initialises the route_dict attribute"""
        for square in self.dijk_grid:
            self.route_dict[square] = find_route(self.dijk_grid, square, self.exit_square)

    def initialise_square_grid(self, display):
        """Initialises the square_grid attribute"""
        screenWidth, screenHeight = display.get_size()
        squarelen = int(screenHeight / self.height)  # Length of each square on the grid

        gridStartX = int(screenWidth / 2 - screenHeight / 2)
        gridStartY = 0

        for i in range(self.height):
            row = []
            for j in range(self.width):
                sqrX = gridStartX + squarelen * j
                sqrY = gridStartY + squarelen * i
                greySqr = pygame.Rect(sqrX, sqrY, squarelen, squarelen)
                sqr = Square(greySqr)
                row.append(sqr)
            self.square_grid.append(row)

    def initialise_exit(self):
        """Adds the Exit to the square_grid"""
        try:
            sqr = self.square_grid[self.exit_square[0]][self.exit_square[1]]
            w, h = sqr.surface.width, sqr.surface.height
            rect = pygame.Rect(sqr.surface.x, sqr.surface.y, w, h)
            self.square_grid[self.exit_square[0]][self.exit_square[1]] = Exit(rect)
        except(IndexError):
            print("Instance variable square_grid has not been intialised properly.  Please call the method initialise_square_grid to initialise it.")

    def initialise_spawner(self):
        """Adds the Spawner to the square_grid"""
        sqr = self.square_grid[self.spawner_square[0]][self.spawner_square[1]]
        w, h = sqr.surface.width, sqr.surface.height
        rect = pygame.Rect(sqr.surface.x, sqr.surface.y, w, h)
        self.square_grid[self.spawner_square[0]][self.spawner_square[1]] = Spawner(rect)

    def block_square(self, square):
        """Removes a square from dijk_grid when a Tower is built on it"""
        self.dijk_grid.remove_node(square)

    def build_tower(self, range, speed, value, operation, cost, location):
        """Builds a new Tower and blocks off its dijk_grid square"""
        sqr = self.square_grid[location[0]][location[1]]
        w, h = sqr.surface.width, sqr.surface.height
        rect = pygame.Rect(sqr.surface.x, sqr.surface.y, w, h)
        tower = Tower(rect, range, speed, value, operation, cost, location)
        self.square_grid[tower.location[0]][tower.location[1]] = tower
        self.block_square(tower.location)

    def spawn_numemy(self, start_val, coins, speed, weight):
        """Spawns a new Numemy object"""
        sqr = self.square_grid[self.spawner_square[0]][self.spawner_square[1]]
        w, h = sqr.surface.width, sqr.surface.height
        rect = pygame.Rect(sqr.surface.x, sqr.surface.y, w, h)
        numemy = Numemy(rect, start_val, coins, speed, weight)
        numemy.location = self.spawner_square
        self.square_grid[numemy.location[0]][numemy.location[1]] = numemy
        self.numemy_list.append(numemy)

    # Should be called after build_tower
    def update_routes(self, new_square):
        """Updates all routes which pass through a new_square being built upon"""
        for square in self.route_dict:
            if new_square in self.route_dict[square]:
                self.route_dict[square] = find_route(square)


    def update_square(self, oldSquarePos, newSquarePos, squarelen, widthStartingX):
        """Moves the square specified by oldSquarePos to newSquarePos"""

        # Sets the specified square to its new position
        sqr = self.square_grid[oldSquarePos[0]][oldSquarePos[1]]

        # Sets the old position of the square to a square with a rectangle background
        surface = pygame.Rect(sqr.surface.x, sqr.surface.y, sqr.surface.width, sqr.surface.height)
        greySqr = Square(surface)
        self.square_grid[oldSquarePos[0]][oldSquarePos[1]] = greySqr

        
        sqr.surface = pygame.Rect(newSquarePos[1] * squarelen + widthStartingX, newSquarePos[0] * squarelen, sqr.surface.width, sqr.surface.height)
        self.square_grid[newSquarePos[0]][newSquarePos[1]] = sqr