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
def find_route(grid, square, exit_square):
    return find_path(grid, square, exit_square)[0]
