import numpy


# A Grid is a height x width rectangle, where walls is a list of
# squares that cannot be occupied
class Grid:
    def __init__(self, height, width, walls):
        self.height = height
        self.width = width
        self.walls = walls
        self.grid = numpy.zeros((height, width))
