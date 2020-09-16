from dijkstar import Graph, find_path


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
    global grid
    global exit_square
    return find_path(grid, square, exit_square)[0]


# Returns an initial dictionary of routes from all squares
def route_list():
    global grid
    global exit_square
    routes = {}
    for square in grid:
        routes[square] = find_route(square)
    return routes


# Removes a square from the grid when a tower is built on it
def block_square(square):
    global grid
    grid.remove_node(square)


# Builds a new Tower and blocks off its square.
def build_tower(tower):
    global tower_list
    tower_list.append(tower)
    block_square(tower.square)


# Updates all routes which pass through a square being built upon
# Should be run after block_square(new_square)
def update_routes(new_square):
    global grid
    global exit_square
    global route_list
    for square in route_list:
        if new_square in route_list[square]:
            route_list[square] = find_route(square)
