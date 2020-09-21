from Square import Square


class Numemy(Square):
    # 'value' is the current health of the Numemy, initiated at
    # 'start_val'; 'coins' is added to player wealth when Numemy
    # is killed; 'speed' is movement speed; 'square' is the current
    # location, initiated at 'spawn_square'.
    def __init__(self, surface, start_val, coins, speed, weight):
        Square.__init__(self, surface)
        self.value = start_val
        self.coins = coins
        self.speed = speed
        self.location = None
        self.weight = weight

    def next_square(self, grid):
        """Returns the next square on the route from a starting square"""
        if len(grid.route_dict[self.location]) == 1:
            return grid.route_dict[self.location][0]
        else:
            return grid.route_dict[self.location][1]

    def move(self, grid):
        """Moves Numemy to next square in its route"""
        self.location = self.next_square(grid)

    # For when a Numemy reaches the exit_square
    def escape(self, grid):
        grid.lives -= self.weight
        grid.square_grid[self.location[0]][self.location[1]] = Square(EXIT_SQUARE_SURFACE)

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
