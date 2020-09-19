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
        self.location = spawn_square
        self.weight = weight

    def next_square(self):
        """Returns the next square on the route from a starting square"""
        return route_dict[self.location][1]

    def move(self):
        """Moves Numemy to next square in its route"""
        self.location = self.next_square()

    # For when a Numemy reaches the exit_square
    def escape(self):
        global lives
        global square_grid
        lives -= self.weight
        square_grid[self.location[0]][self.location[1]] = Square(EXIT_SQUARE_SURFACE)

    def take_damage(self, operation, damage):
        """When a Numemy is hit"""
        if operation == '+':
            self.value += damage
        elif operation == '-':
            self.value -= damage
        elif operation == '/':
            self.value /= damage
        elif operation == '*':
            self.value *= damage
