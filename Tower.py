from numpy import linalg


class Tower:
    def __init__(self, range, speed, square, value, operation):
        self.range = range
        self.speed = speed
        self.square = square
        self.value = value
        self.operation = operation
        self.level = 1

    def attack(self, numemy):
        global numemy_list
        numemy.take_damage(self.operation, self.value)
        if numemy.value == 0:
            numemy_list.remove(numemy)

    def find_target(self):
        global numemy_list
        for numemy in numemy_list:
            if linalg.norm(numemy.square - self.square) <= self.range:
                return numemy
