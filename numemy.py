from Square import Square

class Numemy(Square):
    def __init__(self, surface, start_val, coins, speed, spawn_square):
        Square.__init__(self, surface)
        self.value = start_val
        self.coins = coins
        self.speed = speed
        self.square = spawn_square

    def next_square(self):
        global route_list
        return route_list[self.square][1]

    def move(self):
        self.square = self.next_square()

    def take_damage(self, operation, damage):
        if operation == '+':
            self.value += damage
        elif operation == '-':
            self.value -= damage
        elif operation == '/':
            self.value /= damage
        elif operation == '*':
            self.value *= damage
