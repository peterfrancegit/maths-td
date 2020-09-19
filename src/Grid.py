from dijkstar import Graph, find_path
from Square import Square
from Numemy import Numemy
from Tower import Tower
from Square import Exit
from Square import Spawner
import pygame

# Dimensions of both the grids
WIDTH = 10
HEIGHT = 10

Lives = None
square_grid = None
dijkstra_grid = None
all_numemies = []
exit_square = None
route_dict = {}


def make_grid(height, width, blocks):
    """Returns graph of a 'height' x 'width' grid with edges between
    neighbouring squares and where nodes in 'blocks' are excluded"""
    grid = Graph()
    for i in range(height):
        for j in range(width):
            if i < height - 1:
                grid.add_edge((i, j), (i + 1, j), 1)
                grid.add_edge((i + 1, j), (i, j), 1)
            if j < width - 1:
                grid.add_edge((i, j), (i, j + 1), 1)
                grid.add_edge((i, j + 1), (i, j), 1)
    for node in blocks:
        grid.remove_node(node)
    return grid


def find_route(square):
    """Returns list of nodes visited in shortest route from square
    to the exit point"""
    global dijkstra_grid
    global exit_square
    return find_path(dijkstra_grid, square, exit_square)[0]


def block_square(square):
    """Removes a square from the grid when a Tower is built on it"""
    global dijkstra_grid
    dijkstra_grid.remove_node(square)


def build_tower(tower):
    """Builds a new Tower and blocks off its square"""
    global square_grid
    square_grid[tower.location[0]][tower.location[1]] = tower
    block_square(tower.location)


def spawn_numemy(numemy):
    """Spawns a new Numemy object"""
    global square_grid
    square_grid[numemy.location[0]][numemy.location[1]] = numemy


# Should be called after block_square and build_tower
def update_routes(new_square):
    """Updates all routes which pass through a square being built upon"""
    global route_dict
    for square in route_dict:
        if new_square in route_dict[square]:
            route_dict[square] = find_route(square)


def initialise_grid(display):
    """Initialises the global grid variables"""
    global dijkstra_grid
    global square_grid
    
    blocks = []
    dijkstra_grid = make_grid(WIDTH, HEIGHT, blocks)

    # Initialises the square grid

    screenWidth, screenHeight = display.get_size()
    squarelen = screenHeight / HEIGHT # Length of each square on the grid

    gridStartX = screenWidth / 2 - screenHeight / 2
    gridStartY = 0

    square_grid = []
    for i in range(HEIGHT):
        row = []
        for j in range(WIDTH):
            sqrX = gridStartX + squarelen * j
            sqrY = gridStartY + squarelen * i
            greySqr = pygame.Rect(sqrX, sqrY, squarelen, squarelen)
            sqr = Square(greySqr)
            row.append(sqr)
        square_grid.append(row)

    # Creates a numemy with the value 6 and puts it into square_grid
    sqr = square_grid[4][0]
    all_numemies.append((4, 0))
    w, h = sqr.surface.width, sqr.surface.height
    rect = pygame.Rect(sqr.surface.x, sqr.surface.y, w, h)
    square_grid[4][0] = Numemy(rect, 6, 0, 3, [], 5)

    # Creates a numemy with the value 3 and puts it into square_grid
    sqr = square_grid[4][1]
    all_numemies.append((4, 1))
    w, h = sqr.surface.width, sqr.surface.height
    rect = pygame.Rect(sqr.surface.x, sqr.surface.y, w, h)
    square_grid[4][1] = Numemy(rect, 3, 0, 3, [], 1)

    # Creates a tower with the gun +1 and puts it into square_grid
    sqr = square_grid[6][2]
    w, h = sqr.surface.width, sqr.surface.height
    rect = pygame.Rect(sqr.surface.x, sqr.surface.y, w, h)
    square_grid[6][2] = Tower(rect, 2, 2, 10, '+', 50, (6, 2))

    # Creates an Exit and puts it into the square_grid
    sqr = square_grid[4][9]
    exit_square = (4, 9)
    w, h = sqr.surface.width, sqr.surface.height
    rect = pygame.Rect(sqr.surface.x, sqr.surface.y, w, h)
    square_grid[4][9] = Exit(rect)

    # Creates a Spawner and puts it into the square_grid
    sqr = square_grid[5][5]
    w, h = sqr.surface.width, sqr.surface.height
    rect = pygame.Rect(sqr.surface.x, sqr.surface.y, w, h)
    square_grid[5][5] = Spawner(rect)


def initialise_route_dict():
    """Initialises the global route_dict variable"""
    global dijkstra_grid
    global route_dict
    for square in dijkstra_grid:
        route_dict[square] = find_route(square)
