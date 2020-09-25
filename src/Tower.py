from numpy import linalg
from Square import Square
from Numemy import Numemy
import math


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

    def calculate_dist(self, numemyPos, towerPos):
        dist = math.sqrt((towerPos[0] - numemyPos[0])**2 + (towerPos[1] - numemyPos[1])**2)
        return abs(dist)

    def attack(self, grid, numemy):
        """Damages a Numemy, and kills it if health is 0"""
        numemy.take_damage(self.operation, self.value)
        if numemy.value <= 0:
            grid.square_grid[numemy.location[0]][numemy.location[1]].remove(numemy)

    def find_targets(self, grid):
        """Returns a Numemy within range, if one exists"""
        targets = []
        for num_loc in grid.num_loc_list:
            square = grid.square_grid[num_loc[0]][num_loc[1]]
            for entity in square:
                if isinstance(entity, Numemy):
                    dist = self.calculate_dist(entity.location, self.location)
                    if dist <= self.range:
                        targets.append(entity)
        return targets
