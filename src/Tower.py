from Square import Square
from Numemy import Numemy
import math


class Tower(Square):
    # 'range' is the radius of the circle the Tower attacks within;
    # 'speed' is how often it attacks;
    # 'cost' is removed from player's wealth;
    # 'level' is 1, 2 or 3 and increases range and speed.
    def __init__(self, surface, value, operation, cost, location):
        Square.__init__(self, surface)
        self.range = 3
        self.speed = 1
        self.value = value
        self.operation = operation
        self.cost = cost
        self.location = location
        self.level = 1

    def calculate_dist(self, numemyPos, towerPos):
        dist = math.sqrt((towerPos[0] - numemyPos[0])**2 + (towerPos[1] - numemyPos[1])**2)
        return abs(dist)

    def attack(self, grid, numemy):
        """Damages a Numemy, and kills it if health is 0"""
        numemy.take_damage(self.operation, self.value)
        if numemy.value == 0:
            grid.square_grid[numemy.location[0]][numemy.location[1]].remove(numemy)
            grid.souls += souls

    def find_targets(self, grid):
        """Returns a Numemy within range, if one exists"""
        for num_loc in grid.num_loc_list:
            square = grid.square_grid[num_loc[0]][num_loc[1]]
            for entity in square:
                if isinstance(entity, Numemy):
                    dist = self.calculate_dist(entity.location, self.location)
                    if dist <= self.range:
                        return entity
        return None

    def upgrade(self):
        self.level += 1
        self.range *= 1.5
        self.speed *= 1.5
