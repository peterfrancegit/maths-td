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
        global numemy_list
        numemy.take_damage(self.operation, self.value)
        if numemy.value == 0:
            numemy_list.remove(numemy)

    def find_target(self):
        """Returns a Numemy within range, if one exists"""
        global numemy_list
        for numemy in numemy_list:
            if linalg.norm(numemy.square - self.square) <= self.range:
                return numemy
