from numpy import linalg
from Square import Square


class Tower(Square):
    # 'range' is the radius of the circle the Tower attacks within;
    # 'speed' is how often it attacks; 'square' is the location;
    # 'cost' is removed from player's wealth.
    def __init__(self, surface, range, speed, square, value, operation, cost):
        Square.__init__(self, surface)
        self.range = range
        self.speed = speed
        self.square = square
        self.value = value
        self.operation = operation
        self.level = 1
        self.cost = cost

    # Damages a Numemy, and kills it if health is 0
    def attack(self, numemy):
        global numemy_list
        numemy.take_damage(self.operation, self.value)
        if numemy.value == 0:
            numemy_list.remove(numemy)

    # Returns a Numemy within range, if one exists
    def find_target(self):
        global numemy_list
        for numemy in numemy_list:
            if linalg.norm(numemy.square - self.square) <= self.range:
                return numemy
