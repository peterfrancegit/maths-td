from Square import Square


class Numemy(Square):
    # 'value' is the current health of the Numemy, initiated at
    # 'start_val'; 'souls' is added to Player souls when Numemy
    # is killed; 'speed' is movement speed; 'weight' is subtracted
    # from Player lives if the Numemy escapes.
    def __init__(self, surface, start_val, souls, speed, weight):
        Square.__init__(self, surface)
        self.value = start_val
        self.souls = souls
        self.speed = speed
        self.location = None
        self.weight = weight

    def next_square(self, grid):
        """Returns the next square on the route from a starting square"""
        if len(grid.route_dict[self.location]) == 1:
            return grid.route_dict[self.location][0]
        else:
            return grid.route_dict[self.location][1]

    # For when a Numemy reaches the exit_square
    def escape(self, player):
        """Reduces Player lives and deletes Numemy object upon escaping"""
        player.lives -= self.weight

    def take_damage(self, operation, damage):
        """Changes the value of a Numemy"""
        if operation == '+':
            self.value += damage
        elif operation == '-':
            self.value -= damage
        elif operation == '/':
            self.value /= damage
        elif operation == '*':
            self.value *= damage
