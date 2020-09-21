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
    def __init__(self, height, width, blocks, exit_square):
        self.route_dict = {}
        self.height = height
        self.width = width
        self.blocks = blocks
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
        squarelen = screenHeight / self.height  # Length of each square on the grid

        gridStartX = screenWidth / 2 - screenHeight / 2
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

    def block_square(self, square):
        """Removes a square from dijk_grid when a Tower is built on it"""
        self.dijk_grid.remove_node(square)

    def build_tower(self, tower):
        """Builds a new Tower and blocks off its dijk_grid square"""
        self.square_grid[tower.location[0]][tower.location[1]] = tower
        self.block_square(tower.location)

    def spawn_numemy(self, numemy):
        """Spawns a new Numemy object"""
        self.square_grid[numemy.location[0]][numemy.location[1]] = numemy
        self.numemy_list.append(numemy)

    # Should be called after build_tower
    def update_routes(self, new_square):
        """Updates all routes which pass through a new_square being built upon"""
        for square in self.route_dict:
            if new_square in self.route_dict[square]:
                self.route_dict[square] = find_route(square)


        # Creates an Exit and puts it into the square_grid
        sqr = square_grid[4][9]
        exit_square = (4, 9)
        w, h = sqr.surface.width, sqr.surface.height
        rect = pygame.Rect(sqr.surface.x, sqr.surface.y, w, h)
        square_grid[4][9] = Exit(rect)

        # Creates a numemy with the value 6 and puts it into square_grid
        sqr = square_grid[4][0]
        w, h = sqr.surface.width, sqr.surface.height
        rect = pygame.Rect(sqr.surface.x, sqr.surface.y, w, h)
        spawn_numemy(Numemy(rect, 6, 0, 3, (4, 0), 5))

        # Creates a numemy with the value 3 and puts it into square_grid
        sqr = square_grid[4][1]
        w, h = sqr.surface.width, sqr.surface.height
        rect = pygame.Rect(sqr.surface.x, sqr.surface.y, w, h)
        spawn_numemy(Numemy(rect, 3, 0, 3, (4, 1), 1))

        # Creates a tower with the gun +1 and puts it into square_grid
        sqr = square_grid[6][2]
        w, h = sqr.surface.width, sqr.surface.height
        rect = pygame.Rect(sqr.surface.x, sqr.surface.y, w, h)
        build_tower(Tower(rect, 2, 2, 10, '+', 50, (6, 2)))

        # Creates a Spawner and puts it into the square_grid
        sqr = square_grid[5][5]
        w, h = sqr.surface.width, sqr.surface.height
        rect = pygame.Rect(sqr.surface.x, sqr.surface.y, w, h)
        square_grid[5][5] = Spawner(rect)
