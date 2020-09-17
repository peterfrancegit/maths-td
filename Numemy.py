from Square import Square


class Numemy(Square):
    # 'value' is the current health of the Numemy, initiated at
    # 'start_val'; 'coins' is added to player wealth when Numemy
    # is killed; 'speed' is movement speed; 'square' is the current
    # location, initiated at 'spawn_square'.
    def __init__(self, surface, start_val, coins, speed, spawn_square, weight):
        Square.__init__(self, surface)
        self.value = start_val
        self.coins = coins
        self.speed = speed
        self.square = spawn_square
        self.weight = weight

    # Returns the next square on the route from a starting square.
    def next_square(self):
        global route_dict
        return route_dict[self.square][1]

    # Moves Numemy to next square in its route.
    def move(self):
        self.square = self.next_square()

    # Used when a Tower damages a Numemy.
    def take_damage(self, operation, damage):
        if operation == '+':
            self.value += damage
        elif operation == '-':
            self.value -= damage
        elif operation == '/':
            self.value /= damage
        elif operation == '*':
            self.value *= damage
