from dijkstar import Graph, find_path
from Square import Square
import pygame

# Dimensions of both the grids
WIDTH = 10
HEIGHT = 10

square_grid = None
dijkstra_grid = None
exit_square = None
numemy_list = []
tower_list = []
route_list = {}


# Returns a graph based on a 'height' x 'width' grid, where
# 'blocks' is a list of the indices of walled off squares.
def make_grid(height, width, blocks):
    grid = Graph()
    for i in range(height - 1):
        if (i, width - 1) and (i + 1, width - 1) not in blocks:
            grid.add_edge((i, width - 1), (i + 1, width - 1), 1)
            grid.add_edge((i + 1, width - 1), (i, width - 1), 1)
        for j in range(width - 1):
            if (i, j) not in blocks:
                if (i, j + 1) not in blocks:
                    grid.add_edge((i, j), (i, j + 1), 1)
                    grid.add_edge((i, j + 1), (i, j), 1)
                if (i + 1, j) not in blocks:
                    grid.add_edge((i, j), (i + 1, j), 1)
                    grid.add_edge((i + 1, j), (i, j), 1)
    for j in range(width - 1):
        if (height - 1, j) and (height - 1, j + 1) not in blocks:
            grid.add_edge((height - 1, j), (height - 1, j + 1), 1)
            grid.add_edge((height - 1, j + 1), (height - 1, j), 1)
    return grid


# Returns a list of nodes visited in the shortest route from
# a chosen square to the exit point.
def find_route(square):
    global dijkstra_grid
    global exit_square
    return find_path(dijkstra_grid, square, exit_square)[0]


# Returns an initial dictionary of routes from all squares
def route_list():
    global dijkstra_grid
    global exit_square
    routes = {}
    for square in dijkstra_grid:
        routes[square] = find_route(square)
    return routes


# Removes a square from the grid when a tower is built on it
def block_square(square):
    global dijkstra_grid
    dijkstra_grid.remove_node(square)


# Builds a new Tower and blocks off its square.
def build_tower(tower):
    global tower_list
    tower_list.append(tower)
    block_square(tower.square)


def spawn_numemy(numemy):
    global numemy_list
    numemy_list.append(numemy)


# Updates all routes which pass through a square being built upon
# Should be run after block_square(new_square)
def update_routes(new_square):
    global dijkstra_grid
    global exit_square
    global route_list
    for square in route_list:
        if new_square in route_list[square]:
            route_list[square] = find_route(square)


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


def initialise_route_list(display):
    """Initialises the global route_list variable"""
    global dijkstra_grid
    global exit_square
    global route_list

    blocks = []

    dijkstra_grid = make_grid(WIDTH, HEIGHT, blocks)

    for square in dijkstra_grid:
        route_list[square] = find_route(square)



