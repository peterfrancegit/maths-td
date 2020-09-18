from numpy import linalg
from Square import Square


class Tower(Square):
    # 'range' is the radius of the circle the Tower attacks within;
    # 'speed' is how often it attacks; 'square' is the location;
    # 'cost' is removed from player's wealth.
    def __init__(self, surface, range, speed, value, operation, cost, location):
        Square.__init__(self, surface)
        self.range = range
        self.speed = speed
        self.value = value
        self.operation = operation
        self.level = 1
        self.cost = cost
        self.location = location

    def attack(self, numemy):
        """Damages a Numemy, and kills it if health is 0"""
        global square_grid
        numemy.take_damage(self.operation, self.value)
        if numemy.value == 0:
            square_grid[numemy.location[0]][numemy.location[1]] = Square(EMPTY_SURFACE)

    def find_target(self):
        """Returns a Numemy within range, if one exists"""
        global square_grid
        for square in square_grid:
            if isinstance(square, Numemy):
                if linalg.norm(numemy.location - self.location) <= self.range:
                    return numemy